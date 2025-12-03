# Video Integration Guide

Systematic capture and pedagogical integration of high-quality video resources in course content.

## Overview

This guide documents how to systematically include videos (TED talks, expert presentations, demonstrations) in course research and content generation with minimal overhead and clear pedagogical purpose.

### Why Videos?

**Unique pedagogical value:**
- Researchers explaining their own theories (authenticity, credibility)
- Visual demonstrations that text cannot convey
- Emotional engagement and storytelling
- Alternative learning modality for diverse learners

**When videos work best:**
- Topics with well-known expert presentations (TED, conference keynotes)
- Visual/physical demonstrations (body language, design, process)
- Motivational/inspirational content (growth mindset, leadership)
- Complex concepts clarified through narrative

**When to skip videos:**
- Highly technical frameworks better explained in text
- No quality videos exist for the specific topic
- Articles already provide excellent comprehensive coverage
- Time-constrained research session

---

## Research Phase: Finding Quality Videos

### Integration in Desktop Research Workflow

Videos are discovered during Claude Desktop research as **Stage 1.5** (optional):

1. **Article Discovery** (Stage 1) - Find 10-15 article candidates
2. **Video Discovery** (Stage 1.5) - **NEW** - Find 0-2 video candidates (+5-10 min)
3. **Article Quick Filter** (Stage 2) - Narrow to 5-6 articles
4. **Article Content Validation** (Stage 3) - Deep check 2-3 finalists
5. **Present to User** (Stage 4) - User selects final 2 articles + 0-2 videos

**Time Investment:** +5-10 minutes per week (10-20% increase on 30-50 min baseline)

---

### Video Discovery Process (10 min max)

#### Step 1: Quick Search (2 min)

**Search strategies:**
```
"[topic] TED talk"
"[seminal author name] [framework] video"
site:youtube.com [topic] "official" OR "verified"
```

**Example searches:**
- Growth mindset: `"Carol Dweck" growth mindset TED`
- Persuasion: `"Robert Cialdini" influence video`
- Leadership: `"Simon Sinek" leadership TED talk`

#### Step 2: Quality Filter (2 min)

Apply checklist:
- ✓ **Duration:** 3-15 min ideal (<20 min maximum for in-class)
- ✓ **Source credibility:** TED, universities, verified channels, official organizations
- ✓ **Recency:** 2018+ (unless historical/seminal presentation)
- ✓ **Accessibility:** Works in Vietnam, has subtitles/captions
- ✓ **Concept coverage:** Addresses ≥1 required concept clearly

#### Step 3: Content Match (3 min)

- Watch at 2x speed or skim with player preview
- Check: Does it cover ≥1 required concept clearly?
- Assess: Does it provide unique value vs. articles?
- Decide: Required candidate, Optional candidate, or Skip

#### Step 4: Document (2 min)

Fill video metadata template:
- URL (direct link) + Backup URL (mirror/alternative)
- Duration (MM:SS format)
- Creator/Speaker (name, credentials)
- Source/Platform (TED, YouTube official, university, etc.)
- Publication date
- Tier classification (Primary vs Supplementary)
- Suggested usage (Required vs Optional candidate)
- 2-3 sentence content summary (for obsolescence fallback)
- Discussion prompts (if suggesting as required)

---

## Decision Matrix: Video Classification

### Tier System

| Tier | Definition | Examples |
|------|------------|----------|
| **Primary** | Authoritative expert (researcher, author, industry leader) | Carol Dweck on growth mindset, Simon Sinek on leadership |
| **Supplementary** | High teaching quality but not original researcher | Animated explainers, case studies, demonstrations |

### Usage System

| Usage | When to Use | Student Expectation |
|-------|-------------|---------------------|
| **Required** | Essential for understanding, provides unique value | Must watch, assessed content |
| **Optional** | Enrichment, alternative explanation, deeper dive | Not assessed, for interested learners |

### Decision Tree

```
Is video by the researcher/author who created the theory?
├─ YES → PRIMARY tier
└─ NO → Is it high-quality teaching content?
    ├─ YES → SUPPLEMENTARY tier
    └─ NO → Skip video

Does video cover ≥1 concept better than articles can?
├─ YES → Consider REQUIRED
└─ NO → Consider OPTIONAL (or skip)

Is video ≤15 min?
├─ YES → In-class viewing candidate
└─ NO (15-30 min) → Pre-work assignment candidate
    └─ NO (>30 min) → Split, make optional, or skip
```

---

## Validation Criteria

### Automatic Validation (Import Stage)

**Count Check:**
- ✓ 0-2 videos per week (PASS)
- ✗ >2 videos (FAIL - cognitive overload)

**Metadata Completeness:**
- ✓ Creator/Speaker present
- ✓ URL accessible (quick HEAD request)
- ✓ Duration specified
- ✓ Source/Platform specified
- ✓ Tier (Primary/Supplementary) specified
- ✓ Usage (Required/Optional candidate) specified

**Content Check:**
- ✓ ≥1 concept covered (videos supplement, don't need ALL concepts like articles)
- ✓ "Why selected" rationale present
- ✓ Key content summary present (2-3 sentences minimum)

**Accessibility:**
- ✓ Open access (YouTube, TED, institutional sites)
- ✗ Paywalled videos rejected (unlike articles where seminal paywalls acceptable)

**Duration:**
- ✓ <20 min (acceptable)
- ⚠ 20-30 min (warning - long for in-class, suggest pre-work)
- ✗ >30 min (fail - too long, suggest splitting or making optional)

### Key Differences from Article Validation

| Aspect | Articles | Videos |
|--------|----------|--------|
| Concept coverage | ALL concepts required | ≥1 concept sufficient |
| Paywalled content | OK for seminal works | Never acceptable |
| Length limits | None | <20 min enforced |
| Quantity | Exactly 4 per week | 0-2 per week (flexible) |
| Required status | Always required | Mixed (some required, some optional) |

---

## Integration Patterns: How Videos Appear in Lectures

### Pattern A: Required Video - In-Class Viewing (≤15 min)

**Use when:**
- Video is PRIMARY tier
- Researcher explaining own theory
- Essential for understanding core concept

**Lecture format:**
```xml
<slide number="X" layout="content" title="Video Title">

## [Video Title]

**[VIDEO: [Speaker Name] - "[Video Title]"]**
**Video link:** [URL]
**Duration:** [MM:SS]

**Before watching:** [Pre-viewing question to prime attention]

<speaker-notes>
Setup (30 sec): Introduce [Speaker] and their credentials. Prime with question: "[Question]". Direct attention to [key moment] in the video.

After video: Quick debrief asking "What stood out to you?" Take 2-3 responses. Connect to next section: [How video relates to upcoming content].

Transition: "Now that we've seen [speaker]'s explanation, let's dive deeper into..."
</speaker-notes>

</slide>
```

**Example:** Carol Dweck TED talk (10 min) in Week 9 Growth Mindset lecture

**Slide counting:** Videos >5 min count as 1 slide toward 22-30 target

---

### Pattern B: Optional Video - Supplementary Resources

**Use when:**
- Video is SUPPLEMENTARY tier
- Enrichment for interested students
- Not essential for assessed content

**Lecture format:**
```xml
<slide number="X" layout="content" title="Further Resources">

## Further Resources (Optional)

**Videos:**
- [Speaker] – "[Title]" ([Duration]) - [URL]
  - Why watch: [1 sentence benefit]
- [Speaker] – "[Title]" ([Duration]) - [URL]
  - Why watch: [1 sentence benefit]

**Not required** - All assessed material covered in readings and lecture.

<speaker-notes>
Brief mention: "For those interested in going deeper, I've linked two excellent videos on this topic. They're optional but highly recommended if you want to see these concepts in action."
</speaker-notes>

</slide>
```

**Example:** Angela Duckworth TED talk (6 min) as optional supplement to required Dweck video

**Slide counting:** Optional resource slides don't count toward 22-30 if placed at end

---

### Pattern C: Pre-Work Assignment (15-30 min video)

**Use when:**
- Video is long but valuable (15-30 min)
- Better as homework than in-class time
- Provides foundation for next class discussion

**Lecture format:**
```xml
<slide number="X" layout="content" title="Pre-Class Preparation">

## Pre-Class Preparation

**Required Viewing Before Next Class:**

**VIDEO:** [Speaker] - "[Title]"
- Duration: [MM:SS]
- Link: [URL]

**Your task:**
1. Watch the full video
2. Note: [specific aspects to focus on]
3. Prepare to discuss: [reflection question]

<speaker-notes>
Assignment instruction: "For next week's class, you must watch [Speaker]'s talk on [topic]. It's 18 minutes - watch it in one sitting and take notes on [specific aspect]. We'll start next class with a discussion of what you learned."

[NOTE FOR NEXT WEEK'S LECTURE: Begin with 5-min video debrief. Quick poll on video content, then connect to that week's topic.]
</speaker-notes>

</slide>
```

**Example:** Simon Sinek "Start With Why" (18 min) as required pre-work before entrepreneurship guest speaker

**Slide counting:** Pre-work assignment slides count as 1 slide

---

## Obsolescence Handling

Videos are more fragile than articles (copyright takedowns, platform changes, geographic restrictions).

### Resilience Strategies

**1. Backup URLs**
Always provide alternative link:
- TED talks: Both TED.com + YouTube mirror
- University lectures: Official channel + institutional site
- Conference talks: Multiple hosting platforms

**2. Content Summaries**
2-3 sentence summary enables fallback:
- If video deleted, instructor can explain key points from summary
- Future research can find replacement videos using summary
- Summary enables assessment of teaching value

**3. Notable Moments**
Document specific timestamps:
- "At 3:45 - Dweck explains 'not yet' framing"
- "At 7:20 - Case study of Chicago high school intervention"

Enables quick quality check and instructor preview.

**4. Quotable Lines**
Preserve memorable quotes:
- Can be used even if video unavailable
- Provides teaching value independently
- Helps assess video quality during research

---

## Platform Accessibility Matrix

### Vietnam Context

| Platform | Accessible? | Subtitles? | Notes |
|----------|-------------|------------|-------|
| **TED.com** | ✓ Yes | ✓ Yes (multi-language) | Ideal - reliable, subtitled, edu-focused |
| **YouTube** | ✓ Yes | ✓ Usually (auto + manual) | Check "official" or "verified" channels |
| **Vimeo** | ✓ Yes | ~ Variable | Less common, check accessibility |
| **Coursera/edX** | ✓ Yes | ✓ Yes | Edu platforms, usually accessible |
| **LinkedIn Learning** | ✗ May require login | ✓ Yes | Avoid unless institutional access |
| **Facebook** | ~ Unreliable | ✗ No | Avoid - poor edu experience |
| **University sites** | ✓ Usually | ~ Variable | Check institutional barriers |

**Best practice:** Prioritize TED and verified YouTube channels for maximum accessibility.

---

## Examples from PPDK66B Course

### Week 1: Introduction & Future of Work

**Video:** WEF Future of Jobs Report 2025 (3 min)
- **Tier:** Supplementary (official organization summary)
- **Usage:** Optional (data visualization)
- **Integration:** Pattern B (supplementary resources)
- **Why:** Visual data presentation supplements Deloitte 2024 article

### Week 9: Growth Mindset & Adaptability

**Video 1:** Carol Dweck - "The Power of Believing That You Can Improve" (10 min)
- **Tier:** Primary (researcher explaining own theory)
- **Usage:** Required (essential for understanding)
- **Integration:** Pattern A (in-class viewing after concept introduction)
- **Why:** Dweck herself explaining core theory with student examples; emotional engagement supplements article statistics

**Video 2:** Angela Duckworth - "Grit: The Power of Passion and Perseverance" (6 min)
- **Tier:** Supplementary (related concept, not core)
- **Usage:** Optional (enrichment)
- **Integration:** Pattern B (supplementary resources at end)
- **Why:** Extends growth mindset to grit concept; optional reinforcement

### Week 10: Entrepreneurship & Guest Speaker

**Video:** Simon Sinek - "Start With Why: How Great Leaders Inspire Action" (18 min)
- **Tier:** Primary (thought leader explaining own framework)
- **Usage:** Required (pre-work assignment)
- **Integration:** Pattern C (required viewing before guest speaker)
- **Why:** Golden Circle framework foundation for entrepreneurial thinking; too long for in-class, perfect as prep

---

## Workflow Impact Summary

### Time Investment Per Week

**Research (Claude Desktop):**
- Current baseline: 30-50 min (4 articles)
- With videos: 35-60 min (+5-10 min video discovery)
- **Overhead:** 10-20% increase

**Validation (Claude Code):**
- Current: 1-2 min
- With videos: 1.5-2.5 min (+30 sec video checks)
- **Overhead:** Negligible

**Generation (Claude Code):**
- No change (reads videos from research like articles)

### Benefits

1. **Systematic capture** - No more ad-hoc video additions during writing
2. **Quality control** - All videos validated before integration
3. **Pedagogical clarity** - Required/optional distinction explicit
4. **Obsolescence resilience** - Backup URLs + content summaries
5. **Instructor flexibility** - Desktop suggests, Code decides final usage

### Constraints Enforced

- 0-2 videos per week (prevents overload)
- Open access only (no paywalled videos)
- <20 min duration (<15 min ideal)
- ≥1 concept coverage minimum
- Required vs optional must be specified

---

## Cross-References

**Related documentation:**
- **Research workflow:** `docs/RESEARCH-HANDOFF-GUIDE.md`
- **Content generation:** `.claude/skills/content-generation/lecture-structure.md`
- **Import validation:** `.claude/commands/import-research.md`
- **Research skill:** `.claude/skills/research/SKILL.md`
- **Research template:** `.claude/templates/desktop-course-research-template.md`

**Critical files for video integration:**
1. Desktop research template (video metadata section)
2. Research skill (Stage 1.5 Video Discovery)
3. Import validation (video checks)
4. Lecture structure (3 integration patterns)
5. This guide (comprehensive reference)
