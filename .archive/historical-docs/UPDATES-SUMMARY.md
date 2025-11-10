# System Updates Summary

Updates made to accommodate institutional access policies, grading system flexibility, Vietnamese ESL support, and Vietnamese market context.

---

## 1. Article Accessibility Policy - UPDATED ✓

### Previous Policy:
- **STRICT**: Only openly accessible articles (no paywalls)
- All paywalled content rejected

### New Policy:
- **Freely accessible:** No barriers → EXCELLENT
- **Institutional access:** Requires university login → **ACCEPTABLE for seminal works**
- **Paywall only:** Cannot access even with institution → REJECT

### Seminal Work Criteria:
- Must have 1000+ citations OR be field-defining
- Students can access via university library database
- Clearly marked as "Requires institutional access" in syllabus

### Files Updated:
- `.claude/commands/research-topic.md`
- `.claude/commands/validate-article-content.md` (implicit)
- Added Vietnamese context research searches

**Rationale:** Seminal foundational works (e.g., Barney's RBV, Porter's classic articles) are often behind paywalls but are essential for academic rigor. University library access makes these available to students.

---

## 2. Grading System Flexibility - NEW ✓

### Problem Addressed:
Different institutions use different grading scales (US 60% pass vs UK 40% pass)

### Solution Implemented:

**Created:** `templates/grading-systems.md`
- Complete reference for US, UK, ECTS, and Vietnamese systems
- Includes grade breakdowns, cultural notes, and rubric alignment guidance

**Updated:** `templates/syllabus-base-template.md`
- Changed from hardcoded US system to placeholder:
  - `{{GRADING_SCALE_TABLE}}`
  - `{{GRADING_SYSTEM}}`
  - `{{PASS_THRESHOLD}}`

**Updated:** `.claude/commands/generate-syllabus.md`
- Added Step 1 question: "Which grading system does your institution use?"
- Options: US System (60% pass), UK System (40% pass), Vietnamese Adapted, Other
- Guides selection of appropriate grading scale table

### Grading Systems Documented:

**US System (60% pass):**
| Grade | % Range |
|-------|---------|
| A | 94-100 |
| B | 80-89 |
| C | 70-79 |
| D | 60-69 (pass) |
| F | <60 |

**UK System (40% pass):**
| Classification | % Range |
|----------------|---------|
| First Class | 70-100 |
| Upper Second (2:1) | 60-69 |
| Lower Second (2:2) | 50-59 |
| Third Class | 40-49 |
| Fail | <40 |

**Vietnamese Adapted:**
- Varies by institution
- Often 40-60% pass threshold
- May use 10-point or 4.0 scale

**Critical Note:** Rubrics must align with grading scale!
- UK "Excellent" = 70%+
- US "Excellent" = 90%+

---

## 3. Vietnamese ESL Support - Key Vocabulary Translations - NEW ✓

### Problem Addressed:
Vietnamese students learning in English as second language need vocabulary priming for complex technical terms

### Solution Implemented:

**Created:** `templates/vocabulary-translation-template.md`
- Complete guide for creating vocabulary translation slides
- Translation research process
- Quality verification methods
- Examples for different disciplines

**Updated:** `.claude/commands/generate-week.md`
- Opening section now includes **Key Vocabulary slide (Từ vựng quan trọng)**
- Must be Slide 2 (after hook, before learning objectives)
- 5-8 key terms with Vietnamese translations
- Pronunciation guides and context examples
- Timing: 3-4 minutes

### Vocabulary Slide Format:

```markdown
**SLIDE 2: Key Vocabulary / Từ vựng quan trọng**

**Today's Key Terms:**

1. **Strategy** → Chiến lược
   - *Pronunciation:* /CHee-EN luh-erk/
   - *Context:* "Our company's strategy is to enter new markets"

2. **Competitive Advantage** → Lợi thế cạnh tranh
   - *Pronunciation:* /ler-ee tay kang tranh/
   - *Context:* "Low costs give us competitive advantage"

[... 5-8 terms total]
```

### Translation Resources:
- tracau.vn, vdict.com (business dictionaries)
- Vietnamese business textbooks
- Vietnamese business publications (vnexpress.net/business)
- WebSearch verification: "[term]" "Vietnamese translation" business

### Selection Criteria:
- Central to topic (used multiple times)
- Technically complex (not everyday English)
- Essential for assessments
- NOT basic words students likely know

**Impact:** Significantly improves comprehension for ESL students. Priming with vocabulary before content helps students follow complex English lectures.

---

## 4. Vietnamese Market Research - REQUIRED ✓

### Problem Addressed:
Need culturally relevant, regionally contextualized examples for Vietnamese students

### Solution Implemented:

**Updated:** `.claude/commands/research-topic.md`
- Added Stage 1 search category: "Vietnamese context research"
- Search queries added:
  - `[topic] Vietnam business`
  - `[concept] Vietnamese market`
  - `[topic] ASEAN application`
  - `[key concept] Southeast Asia`
  - `site:vn [topic] English`

**Updated:** `.claude/commands/generate-week.md`
- **REQUIRED** Vietnamese market research integration
- Search queries:
  - `"[topic] Vietnam business 2024"`
  - `"[concept] Vietnamese companies examples"`
  - `"[topic] Southeast Asia"`
  - `"[industry] Vietnam market size 2024"`
  - `"[concept] Vietnam case study English"`
  - `"Vietnam vs [country] [topic]"`

**Goal:** Every lecture should have 2-3 Vietnamese or ASEAN examples

**Note:** Search in English (students' medium of instruction)

### Examples of Vietnamese Context:
- Vietnamese companies (VinGroup, Viettel, Vinamilk, Grab Vietnam)
- Vietnamese market statistics (market size, growth rates)
- ASEAN regional comparisons
- Vietnamese business practices and culture
- Local case studies

### Research Sources:
- Vietnamese business publications (English sections)
- ASEAN business journals
- International articles featuring Vietnamese examples
- Vietnamese university research (English)
- Regional economic reports

**Impact:** Makes content immediately relevant and applicable to students' local business environment. Increases engagement and practical understanding.

---

## 5. Citation Format Update - INTEGRATED ✓

### Previous Format:
References in separate section after each slide

### New Format:
References integrated within slide content

**Updated Files:**
- `lecture_content_instructions.md`
- `.claude/commands/generate-week.md`

### New Citation Style:

```markdown
CONTENT:
[Core concepts with sufficient detail]
[Inline citations throughout (Author, Year)]

Example: "According to Porter (1996), competitive advantage comes from strategic
trade-offs that competitors cannot replicate."

[If source is key to this slide, include full reference at bottom:]
*Porter, M. E. (1996). What is strategy? Harvard Business Review, 74(6), 61-78.
https://hbr.org/1996/11/what-is-strategy*
```

**Also:**
- Complete reference list compiled at end of lecture document
- Students can easily find full citations
- Slides remain clean and professional

**Rationale:** More practical for presentation format. Key references visible on slide when heavily referenced, complete list at end for easy student access.

---

## Summary of All Changes

### Files Created (3 new files):
1. `templates/grading-systems.md` - Complete grading scale reference
2. `templates/vocabulary-translation-template.md` - ESL vocabulary support guide
3. `UPDATES-SUMMARY.md` - This document

### Files Updated (6 files):
1. `.claude/commands/research-topic.md`
   - Institutional access policy for seminal works
   - Vietnamese context research added

2. `.claude/commands/generate-syllabus.md`
   - Grading system selection question added
   - Vietnamese research integration

3. `.claude/commands/generate-week.md`
   - Key vocabulary slide requirement (Slide 2)
   - Vietnamese market research (REQUIRED)
   - Citation format updated
   - Opening expanded to 5-7 slides

4. `templates/syllabus-base-template.md`
   - Grading scale made flexible with placeholders

5. `lecture_content_instructions.md`
   - Citation format updated to integrated style
   - Reference compilation at end

6. `.claude/commands/validate-article-content.md`
   - (Implicitly updated via research-topic changes)

---

## Impact Assessment

### Quality:
- ✓ Maintains academic rigor (seminal works now accessible)
- ✓ Culturally appropriate (Vietnamese context throughout)
- ✓ Pedagogically sound (ESL vocabulary priming)
- ✓ Institutionally flexible (any grading system)

### Student Experience:
- ✓ Better comprehension (vocabulary translations)
- ✓ More relevant (Vietnamese examples)
- ✓ Clear expectations (correct grading scale)
- ✓ Better resources (institutional access to seminal works)

### Instructor Experience:
- ✓ More flexibility (grading system choice)
- ✓ Richer content (Vietnamese context)
- ✓ ESL support built-in (vocabulary slides)
- ✓ Professional citations (integrated format)

---

## Next Steps

### To Use Updated System:

1. **For new courses:**
   - Run `/new-course` as before
   - During `/generate-syllabus`, answer new grading system question
   - System will automatically include Vietnamese research and vocabulary

2. **For existing courses:**
   - Regenerate syllabus with grading system selection
   - Regenerate weeks to include vocabulary slides
   - Vietnamese examples added during regeneration

3. **Quality Check:**
   - Every lecture has vocabulary translation slide
   - 2-3 Vietnamese/ASEAN examples per lecture
   - Grading scale matches institution requirements
   - Seminal works marked as "institutional access"

---

## Testing Recommendations

Before full deployment, test:

1. **Grading System Selection:**
   - Try generating syllabus with UK system
   - Verify correct grade boundaries appear
   - Check rubric alignment

2. **Vocabulary Translation:**
   - Generate Week 1 content
   - Verify Slide 2 has Vietnamese translations
   - Check translation quality with native speaker

3. **Vietnamese Research:**
   - Generate lecture content
   - Verify 2-3 Vietnamese/ASEAN examples present
   - Check relevance and currency

4. **Institutional Access:**
   - Run `/research-topic` for a topic with seminal paywalled work
   - Verify system accepts it with proper labeling
   - Check "institutional access" note appears

---

## Documentation Still Needed:

- `.claude/CLAUDE.md` - Update with all new requirements (in progress)
- Quick reference card for vocabulary translation process
- Example generated content showing all new features

---

*System updated: 2025-11-05*
*All changes backward compatible - existing workflows still function, new features are additions*
