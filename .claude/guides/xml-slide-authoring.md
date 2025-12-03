# XML Slide Authoring Guide

Quick reference for writing lecture slides in XML format.

## File Header (Required) 🔐

Every `lecture-content.md` must start with this exact structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<lecture>
<metadata>
<course>Course Name</course>
<week>N</week>
<topic>Topic Name</topic>
<duration>90 minutes</duration>
<slides>NN</slides>
</metadata>

<slide number="1" ...>
```

**Note:** Course CODE (e.g., BCI2AU) should NOT appear in lecture content - only the course name. Codes change yearly and live in the syllabus only.

**Example:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<lecture>
<metadata>
<course>Business Communication</course>
<week>3</week>
<topic>Structured Business Writing</topic>
<duration>90 minutes</duration>
<slides>28</slides>
</metadata>
```

**To normalize existing files:** `python tools/normalize_lecture_headers.py CODE`

## Slide Structure

```xml
<slide number="1" layout="content" title="Slide Title">

Content goes here (markdown supported)

<speaker-notes>
Notes for the instructor
</speaker-notes>

</slide>
```

## Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `number` | Yes | Slide sequence (1, 2, 3...) |
| `title` | Yes | Displayed in Gemini output |
| `layout` | No | Visual hint (see below) |

## Layout Types

| Layout | When to Use | Example |
|--------|-------------|---------|
| `big-number` | Single statistic | "73% of employees..." |
| `quote` | Citation with attribution | "The best leaders..." — Drucker |
| `framework` | Models, processes | Shannon-Weaver diagram |
| `section-break` | Segment transitions | "Part 2: Application" |
| `content` | Default - mixed content | Bullets, text, lists |

## VS Code Snippets

Type these prefixes and press Tab:

| Prefix | Creates |
|--------|---------|
| `slide` | Generic slide block |
| `slide-big` | Big number slide |
| `slide-quote` | Quote slide |
| `slide-framework` | Framework slide |
| `slide-section` | Section break |
| `slide-objectives` | Learning objectives |
| `notes` | Speaker notes block |

## Speaker Notes Guidelines

**DO write:**
- Pedagogical context ("Students often confuse X with Y")
- Common questions ("Typical question: 'Does this apply to...?'")
- Connections ("This links to Week 3's framework")

**DON'T write:**
- Stage directions ("Pause here", "Wait for silence")
- Emotional instructions ("Let it sink in", "Build suspense")
- Implicit incompetence ("Remember to", "Don't forget")

See `lecture-structure.md` for full tone guidelines.

## Tools

### Validate slides
```bash
python tools/validate_lecture_xml.py COURSE_CODE --week N
```

### Renumber after editing
```bash
python tools/renumber_slides.py COURSE_CODE WEEK_NUMBER
```

### Convert markdown to XML
```bash
python tools/migrate_to_xml_slides.py COURSE_CODE --week N
```

### Generate Gemini prompt
```bash
python tools/generate_gemini_prompts.py COURSE_CODE N
```

## Example: Complete Slide

```xml
<slide number="5" layout="framework" title="Shannon-Weaver Model">

## The Communication Process

**Sender** → **Encoder** → **Channel** → **Decoder** → **Receiver**

↑ **Noise** affects every stage ↑

**Feedback** completes the loop

*Shannon & Weaver (1949)*

<speaker-notes>
The Shannon-Weaver model is foundational but has limitations.
Common student question: "Where does context fit in?"
Answer: Context affects encoding/decoding - good segue to Schramm's model.
This framework appears in Week 4's writing analysis exercise.
</speaker-notes>

</slide>
```

## Troubleshooting

### "Mismatched slide tags"
Check that every `<slide>` has a closing `</slide>`.

### "Missing number attribute"
Ensure format is `number="1"` not `number=1` (quotes required).

### Slides out of order
Run: `python tools/renumber_slides.py COURSE_CODE WEEK`

### Validation errors
Run: `python tools/validate_lecture_xml.py COURSE_CODE -v`
