# H5P Branching Scenario — Build Instructions

## Why a build guide instead of a .h5p file?

H5P Branching Scenario packages require specific internal IDs, library version 
matching, and content type dependencies that vary by your D2L/CloudDeakin H5P 
plugin version. Building directly in the H5P editor is more reliable and takes 
about 15–20 minutes using this structure.

## How to build in CloudDeakin (D2L)

1. Go to your unit → **Content** → **Add Existing Activity** → **H5P**
2. Click **New Content** → search for **Branching Scenario**
3. Build using the structure below

---

## BRANCHING STRUCTURE

### START SCREEN
- **Title:** Interactive Oral Assessments — Guide for Academics
- **Subtitle:** A guided walkthrough — take what you need, skip what you don't.
- **Start button text:** Begin

---

### NODE 1: Welcome (Branching Question)
**Question:** What do you need?

| Choice | Goes to |
|--------|---------|
| Is IOA right for my unit? | Node 2 |
| What exactly is an IOA? | Node 3 |
| I'm ready to design one | Node 4 |
| Logistics and marking | Node 5 |

---

### NODE 2: Is IOA Right for Me? (Course Presentation — 3 slides)

**Slide 1: Quick Stats**
Content (text):
> IOAs are structured professional conversations where students demonstrate understanding in real time.
> - 10 min IOA ≈ 4,000 written words (Colvin & Gaffey)
> - 60% marking time reduction (Shaeri et al.)
> - 19% attendance improvement (Shaeri et al.)
> - No equity gaps found (Davey et al.)
> - Successfully scaled to 800+ students (Griffith)

**Slide 2: Fit Indicators**
Content (text):
> IOA is likely a good fit if your unit involves:
> ✓ Learning outcomes about applying knowledge (not just recall)
> ✓ Academic integrity concerns with current assessments
> ✓ Professional communication or workplace skills
> ✓ Authentic scenarios from industry or practice
> ✓ Need to verify individual understanding
> 
> 3+ indicators = strong fit. Fewer = still worth exploring.

**Slide 3: Branching Question**
**Question:** Where next?

| Choice | Goes to |
|--------|---------|
| Design my IOA | Node 4 |
| What exactly is an IOA? | Node 3 |
| Logistics and marking | Node 5 |

---

### NODE 3: What is an IOA? (Course Presentation — 3 slides)

**Slide 1: Definition**
Content:
> An IOA is a structured, time-limited, professional conversation between a 
> student and an assessor. The student demonstrates understanding by discussing, 
> explaining, and responding to questions — like a workplace consultation.

**Slide 2: IOAs Are / Are Not**
Content (two columns or table):

| IOAs ARE | IOAs ARE NOT |
|----------|-------------|
| Professional conversations | Traditional oral exams |
| Structured around authentic scenarios | Presentations or speeches |
| Testing depth of understanding | Communication skills tests |
| Assessing ability to think on feet | Memorisation exercises |
| An opportunity to probe and follow up | Informal unstructured chats |

**Key distinction:** The critical difference is AUTHENTICITY. In an IOA, the 
conversation mirrors a real professional interaction.

**Slide 3: Branching Question**
**Question:** Where next?

| Choice | Goes to |
|--------|---------|
| Is IOA right for my unit? | Node 2 |
| Design my IOA | Node 4 |

---

### NODE 4: Designing Your IOA (Course Presentation — 4 slides)

**Slide 1: Format Options**
Content (table):

| Format | Best for | Cohort |
|--------|----------|--------|
| Individual viva | Deep probing of knowledge | Any |
| Consultation simulation | Health, law, business | Any |
| Case-based discussion | Analytical disciplines | Any |
| Panel (2 assessors) | Capstone / high-stakes | Smaller |
| Group IOA | Large cohorts, collaboration | Large |

**Slide 2: Duration Guide**
> - 5 min: short, targeted single topic
> - 10 min: standard — equivalent to ~4,000 written words
> - 15 min: extended, complex scenarios
> - 20+ min: in-depth, capstone or professional programs
>
> **Weighting tip:** IOAs work best at 20–40% of the unit.

**Slide 3: Rubric Principles**
> Key principle: Assess the quality of THINKING, not the quality of SPEAKING.
> 
> Common criteria:
> - Content accuracy
> - Depth of reasoning (why, not just what)
> - Application to scenario
> - Adaptability (response to probing/pivot questions)
> - Professional communication (ONLY if it's a learning outcome)
>
> Use 3–4 criteria maximum. Each must be distinguishable at the pass/fail boundary.

**Slide 4: Branching Question**
**Question:** Where next?

| Choice | Goes to |
|--------|---------|
| Logistics and marking | Node 5 |
| Preparing students | Node 6 |
| Back to start | Node 1 |

---

### NODE 5: Logistics (Course Presentation — 3 slides)

**Slide 1: Time & Scheduling**
> **Scheduling formula:** 
> 10-min IOA + 2-min transition = 5 students/hour
> Cohort of 100 = ~20 hours (can parallelise across assessors)
>
> Delivery options: Face-to-face, Online (Teams), or Hybrid

**Slide 2: Recording & Moderation**
> - Record at minimum a moderation sample (every 5th, or all borderline cases)
> - Run a calibration session before marking begins
> - Have all assessors mark 2–3 students independently, then compare
> - Store recordings per your data management plan

**Slide 3: Branching Question**

| Choice | Goes to |
|--------|---------|
| Preparing students | Node 6 |
| Back to start | Node 1 |

---

### NODE 6: Preparing Students (Course Presentation — 2 slides)

**Slide 1: What Students Need**
> Students need:
> ✓ Exact format and duration explained
> ✓ Rubric / marking criteria in advance
> ✓ A practice or mock IOA opportunity
> ✓ Example questions (not actual ones)
> ✓ Technical requirements (if online)
> ✓ How to request accessibility adjustments
>
> **Accessibility:** Extended time, questions provided 5 min early, support 
> person present, written alternative for documented speech disabilities.

**Slide 2: Branching Question**

| Choice | Goes to |
|--------|---------|
| Back to start | Node 1 |
| End — show summary | End Screen |

---

### END SCREEN
- **Title:** You've completed the IOA Guide
- **Text:** Use the information above to plan your IOA implementation. 
  For further support, contact the IOA project team or use the Cogniti agent 
  to get tailored recommendations for your specific unit.

---

## TIPS FOR BUILDING

1. Each "Node" = a content item in the Branching Scenario editor
2. Drag and drop to connect branching paths
3. For "Course Presentation" nodes, add slides using the slide editor
4. The last slide in each Course Presentation should be a "Branching Question"
5. Test all paths before publishing
6. Export the .h5p file to reuse in other units or SharePoint

## EMBEDDING

- **D2L/CloudDeakin:** Native H5P integration — just add as activity
- **SharePoint:** Use H5P.com cloud hosting, embed via iframe
- **Teams:** Add SharePoint page as a Teams tab, or link directly
