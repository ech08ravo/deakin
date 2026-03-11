"""
Reference verification engine.
Parses APA 7th edition references and verifies them against
CrossRef and OpenAlex APIs (both free, no API key needed).
"""

import re
import time
from difflib import SequenceMatcher
import requests

CROSSREF_API = "https://api.crossref.org/works"
OPENALEX_API = "https://api.openalex.org/works"
USER_AGENT = "ReferenceChecker/1.0 (mailto:reference-checker@example.com)"
REQUEST_DELAY = 0.5  # seconds between API calls (polite usage)


def split_references(text):
    """Split pasted text into individual reference strings."""
    text = text.strip()
    if not text:
        return []

    # Try splitting on blank lines first (double newline)
    parts = re.split(r'\n\s*\n', text)
    parts = [p.strip() for p in parts if p.strip()]

    # If that gives only 1 result, try splitting on single newlines
    # but only if lines look like separate references (start with author pattern)
    if len(parts) == 1:
        lines = text.split('\n')
        lines = [l.strip() for l in lines if l.strip()]
        if len(lines) > 1:
            parts = lines

    return parts


def parse_apa_reference(ref_text):
    """
    Extract structured fields from an APA 7th ed reference string.
    Returns a dict with: authors, year, title, doi, raw.
    Fields may be None if extraction fails.
    """
    result = {
        'raw': ref_text,
        'authors': None,
        'year': None,
        'title': None,
        'doi': None,
    }

    # Extract DOI
    doi_match = re.search(
        r'(?:https?://doi\.org/|doi:\s*)(10\.\S+)',
        ref_text, re.IGNORECASE
    )
    if doi_match:
        result['doi'] = doi_match.group(1).rstrip('.')

    # Extract year: (2020) or (2020, January) or (n.d.)
    year_match = re.search(r'\((\d{4})\b', ref_text)
    if year_match:
        result['year'] = year_match.group(1)

    # Extract authors: everything before the year parenthetical
    if year_match:
        authors_text = ref_text[:year_match.start()].strip().rstrip(',').strip()
        if authors_text:
            result['authors'] = authors_text

    # Extract title: text after (year). up to the next period
    # APA titles end with a period, followed by journal/publisher info
    if year_match:
        after_year = ref_text[year_match.end():].lstrip(').').strip()
        # Title is typically the first sentence after the year
        title_match = re.match(r'\.?\s*(.+?\.)', after_year)
        if title_match:
            title = title_match.group(1).strip()
            # Remove trailing period for matching
            title = title.rstrip('.')
            # Remove any italic markers if present
            title = re.sub(r'[*_]', '', title)
            if len(title) > 5:  # Sanity check
                result['title'] = title

    return result


def _similarity(a, b):
    """Calculate string similarity ratio between two strings."""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()


def _check_author_match(parsed_authors, result_authors):
    """Check if at least one author last name matches."""
    if not parsed_authors or not result_authors:
        return False

    # Extract last names from parsed authors string
    parsed_lastnames = set()
    # APA format: "Smith, J. A., & Jones, B."
    for part in re.split(r',\s*&\s*|;\s*', parsed_authors):
        name = part.strip().split(',')[0].strip()
        if name and len(name) > 1:
            parsed_lastnames.add(name.lower())

    # Extract last names from API result
    for author in result_authors:
        family = author.get('family', '').lower()
        if family and family in parsed_lastnames:
            return True

    return False


def _verify_crossref(ref_text, parsed):
    """Query CrossRef API for a reference. Returns best match info or None."""
    params = {'query.bibliographic': ref_text, 'rows': 3}

    # If we have a DOI, try direct lookup first
    if parsed.get('doi'):
        try:
            resp = requests.get(
                f"{CROSSREF_API}/{parsed['doi']}",
                headers={'User-Agent': USER_AGENT},
                timeout=15
            )
            if resp.status_code == 200:
                data = resp.json()
                item = data.get('message', {})
                return _extract_crossref_item(item)
        except requests.RequestException:
            pass

    # Bibliographic search
    try:
        resp = requests.get(
            CROSSREF_API,
            params=params,
            headers={'User-Agent': USER_AGENT},
            timeout=15
        )
        if resp.status_code != 200:
            return None

        data = resp.json()
        items = data.get('message', {}).get('items', [])
        if not items:
            return None

        # Return the best match
        best = None
        best_score = 0
        for item in items[:3]:
            extracted = _extract_crossref_item(item)
            if extracted:
                score = item.get('score', 0)
                if score > best_score:
                    best = extracted
                    best_score = score

        return best

    except requests.RequestException:
        return None


def _extract_crossref_item(item):
    """Extract relevant fields from a CrossRef work item."""
    if not item:
        return None

    titles = item.get('title', [])
    title = titles[0] if titles else None

    authors = item.get('author', [])
    author_names = []
    for a in authors[:5]:  # Limit to first 5
        given = a.get('given', '')
        family = a.get('family', '')
        if family:
            author_names.append(f"{family}, {given}" if given else family)

    # Get year
    year = None
    for date_field in ['published-print', 'published-online', 'issued', 'created']:
        date_info = item.get(date_field, {})
        date_parts = date_info.get('date-parts', [[]])
        if date_parts and date_parts[0] and date_parts[0][0]:
            year = str(date_parts[0][0])
            break

    container = item.get('container-title', [])
    journal = container[0] if container else None

    doi = item.get('DOI')

    return {
        'title': title,
        'authors': author_names,
        'authors_raw': authors,
        'year': year,
        'journal': journal,
        'doi': doi,
        'source': 'CrossRef',
    }


def _verify_openalex(parsed):
    """Query OpenAlex API as a backup verification source."""
    search_term = parsed.get('title') or parsed.get('raw', '')
    if not search_term:
        return None

    # Truncate very long queries
    if len(search_term) > 200:
        search_term = search_term[:200]

    params = {
        'search': search_term,
        'per_page': 3,
    }

    try:
        resp = requests.get(
            OPENALEX_API,
            params=params,
            headers={'User-Agent': USER_AGENT},
            timeout=15
        )
        if resp.status_code != 200:
            return None

        data = resp.json()
        results = data.get('results', [])
        if not results:
            return None

        item = results[0]  # Best match

        # Extract authors
        authorships = item.get('authorships', [])
        author_names = []
        authors_raw = []
        for a in authorships[:5]:
            author_info = a.get('author', {})
            name = author_info.get('display_name', '')
            if name:
                author_names.append(name)
                # Convert to family/given format for matching
                parts = name.rsplit(' ', 1)
                if len(parts) == 2:
                    authors_raw.append({'given': parts[0], 'family': parts[1]})
                else:
                    authors_raw.append({'family': name})

        year = str(item.get('publication_year', '')) or None

        return {
            'title': item.get('title'),
            'authors': author_names,
            'authors_raw': authors_raw,
            'year': year,
            'journal': None,  # OpenAlex nests this differently
            'doi': (item.get('doi') or '').replace('https://doi.org/', ''),
            'source': 'OpenAlex',
        }

    except requests.RequestException:
        return None


def _determine_verdict(parsed, match):
    """
    Compare parsed reference against API match to determine verdict.
    Returns (verdict, confidence, details).
    """
    if not match or not match.get('title'):
        return 'not_found', 0.0, 'No matching record found in academic databases.'

    title_sim = _similarity(parsed.get('title', ''), match['title'])

    # If we couldn't parse a title, try matching the raw text against the result title
    if not parsed.get('title'):
        # Use raw text similarity as a fallback (will be lower)
        raw_sim = _similarity(parsed['raw'], match['title'])
        title_sim = max(title_sim, raw_sim * 1.2)  # Boost slightly

    year_match = (
        parsed.get('year') and match.get('year')
        and parsed['year'] == match['year']
    )

    author_match = _check_author_match(
        parsed.get('authors'), match.get('authors_raw', [])
    )

    # DOI match is the strongest signal
    doi_match = (
        parsed.get('doi') and match.get('doi')
        and parsed['doi'].lower() == match['doi'].lower()
    )

    # Scoring
    if doi_match:
        return 'verified', 1.0, f"DOI match confirmed via {match['source']}."

    if title_sim >= 0.75 and year_match:
        confidence = min(title_sim, 0.99)
        if author_match:
            confidence = min(confidence + 0.05, 0.99)
        return 'verified', confidence, (
            f"Strong title match ({title_sim:.0%}) with matching year "
            f"via {match['source']}."
        )

    if title_sim >= 0.75:
        return 'uncertain', title_sim * 0.8, (
            f"Title matches ({title_sim:.0%}) but year "
            f"{'does not match' if parsed.get('year') else 'could not be compared'} "
            f"via {match['source']}."
        )

    if title_sim >= 0.5:
        return 'uncertain', title_sim * 0.7, (
            f"Partial title match ({title_sim:.0%}) via {match['source']}. "
            f"Manual verification recommended."
        )

    return 'not_found', title_sim, (
        f"Best match has low similarity ({title_sim:.0%}). "
        f"Reference may be fabricated or not indexed."
    )


def verify_reference(ref_text):
    """
    Verify a single reference string.
    Returns a dict with: raw, parsed, verdict, confidence, details, match.
    """
    parsed = parse_apa_reference(ref_text)

    # Try CrossRef first
    match = _verify_crossref(ref_text, parsed)
    verdict, confidence, details = _determine_verdict(parsed, match)

    # If CrossRef didn't find it, try OpenAlex
    if verdict == 'not_found':
        time.sleep(REQUEST_DELAY)
        oa_match = _verify_openalex(parsed)
        if oa_match:
            oa_verdict, oa_confidence, oa_details = _determine_verdict(parsed, oa_match)
            if oa_confidence > confidence:
                match = oa_match
                verdict = oa_verdict
                confidence = oa_confidence
                details = oa_details

    return {
        'raw': ref_text,
        'parsed': {
            'authors': parsed.get('authors'),
            'year': parsed.get('year'),
            'title': parsed.get('title'),
            'doi': parsed.get('doi'),
        },
        'verdict': verdict,
        'confidence': round(confidence, 2),
        'details': details,
        'match': {
            'title': match.get('title') if match else None,
            'authors': match.get('authors', []) if match else [],
            'year': match.get('year') if match else None,
            'journal': match.get('journal') if match else None,
            'doi': match.get('doi') if match else None,
            'source': match.get('source') if match else None,
        } if match else None,
    }


def verify_references(text):
    """
    Verify all references in a pasted text block.
    Returns a list of verification results.
    """
    refs = split_references(text)
    results = []

    for i, ref in enumerate(refs):
        if i > 0:
            time.sleep(REQUEST_DELAY)
        result = verify_reference(ref)
        results.append(result)

    return results
