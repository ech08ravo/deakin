"""
Reference Checker — Flask web app for verifying academic references.
Teachers paste a reference list and the app checks each entry against
CrossRef and OpenAlex to determine if the references are real.
"""

from flask import Flask, render_template, request, jsonify
from verifier import verify_references

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check():
    data = request.get_json()
    if not data or not data.get('references'):
        return jsonify({'error': 'No references provided.'}), 400

    text = data['references'].strip()
    if not text:
        return jsonify({'error': 'Reference text is empty.'}), 400

    results = verify_references(text)

    # Summary stats
    summary = {
        'total': len(results),
        'verified': sum(1 for r in results if r['verdict'] == 'verified'),
        'uncertain': sum(1 for r in results if r['verdict'] == 'uncertain'),
        'not_found': sum(1 for r in results if r['verdict'] == 'not_found'),
    }

    return jsonify({'results': results, 'summary': summary})


if __name__ == '__main__':
    print("\n  Reference Checker is running!")
    print("  Open http://localhost:5000 in your browser.\n")
    app.run(debug=True, port=5000)
