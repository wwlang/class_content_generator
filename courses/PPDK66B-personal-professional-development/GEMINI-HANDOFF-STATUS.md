# Gemini Handoff Status - PPDK66B

**Generated:** December 1, 2025
**Status:** Ready for Gemini processing

---

## Overview

All 10 lecture weeks have Gemini prompts generated and ready for handoff. Weeks 6 and 10 are experiential learning weeks (field trip and guest speaker) with no traditional lectures.

---

## Week-by-Week Status

| Week | Topic | Slides | Status | Videos |
|------|-------|--------|--------|--------|
| **1** | Introduction & Future of Work | 10 | ✅ Ready | WEF video (3 min) |
| **2** | Career Skills in the AI Era | 28 | ✅ Ready | None |
| **3** | Reflection & Reflective Learning | 58 | ✅ Ready | None |
| **4** | Self-Managed Learning | 30 | ✅ Ready | None |
| **5** | Self-Discovery Through Assessment | 23 | ✅ Ready | None |
| **6** | Field Trip (MISA Company) | N/A | ⚠️ Experiential | N/A |
| **7** | Transferable Skills & EI | 22 | ✅ Ready | None |
| **8** | Time, Energy & Habit Management | 25 | ✅ Ready | None |
| **9** | Growth Mindset & Adaptability | 10 | ✅ Ready | Carol Dweck (10 min) + Angela Duckworth (6 min) |
| **10** | Guest Speaker (Ms. Ha Linh) | N/A | ⚠️ Experiential | Simon Sinek pre-work (18 min) |
| **11** | Designing Your Development Plan | 22 | ✅ Ready | None |
| **12** | Integration & Continuous Growth | 27 | ✅ Ready | None |

**Total lecture weeks:** 10
**Total slides:** 255
**Weeks with videos:** 3 (Weeks 1, 9, 10)
**Total videos:** 4 (1 in Week 1, 2 in Week 9, 1 in Week 10)

---

## Instructions for Gemini Processing

### For Each Week:

1. **Navigate to week folder:**
   ```
   courses/PPDK66B-personal-professional-development/weeks/week-NN/
   ```

2. **Open gemini-prompt.md**

3. **Copy everything from `--- PROMPT START ---` to the end**

4. **Paste into Google Gemini**

5. **Wait for complete slide deck generation**

6. **Download as:** `week-NN.pptx` (e.g., `week-01.pptx`, `week-02.pptx`)

7. **Save to the week folder** (same location as gemini-prompt.md)

8. **Run Claude Code command:**
   ```
   /add-speaker-notes PPDK66B [N]
   ```

---

## Special Notes

### Week 1: Introduction & Future of Work
- **Video:** WEF Future of Jobs Report 2025 (3 min)
- **Video placement:** Optional supplementary resource
- **Gemini will:** Create slide with video thumbnail and clickable link

### Week 3: Reflection & Reflective Learning
- **Note:** 58 slides is high - this uses section-based format
- **May need:** Breaking into multiple Gemini sessions if too long
- **Alternative:** Generate in 2-3 batches if Gemini has token limits

### Week 9: Growth Mindset & Adaptability
- **Video 1:** Carol Dweck TED talk (10 min) - REQUIRED, in-class viewing
- **Video 2:** Angela Duckworth TED talk (6 min) - OPTIONAL, supplementary
- **Gemini will:** Create slides with TED branding, speaker photos, prominent links
- **Pattern A (Dweck):** In-class video slide with pre-viewing question
- **Pattern B (Duckworth):** Optional resources slide

### Week 10: Guest Speaker Preparation
- **Video:** Simon Sinek "Start With Why" (18 min) - REQUIRED pre-work
- **Note:** This is in the preparation guide, not the lecture itself
- **No Gemini processing needed** for Week 10 (experiential learning week)

---

## Batch Processing Recommendations

### Option A: Process Sequentially (Recommended)
Process weeks 1-12 in order, one at a time. This allows you to:
- Monitor quality week by week
- Adjust prompts if Gemini misunderstands
- Verify slide counts match expected
- Catch issues early

**Time estimate:** 20-30 min per week = 3-5 hours total

### Option B: Process in Parallel
Open multiple Gemini tabs and process multiple weeks simultaneously:
- Weeks 1-3 in parallel (smaller weeks)
- Weeks 4-5 in parallel (medium weeks)
- Week 7-8 in parallel (standard weeks)
- Weeks 11-12 in parallel (final weeks)

**Time estimate:** 2-3 hours total (faster but harder to monitor)

### Week 3 Special Handling
Week 3 has 58 slides (section-based format). If Gemini hits token limits:
1. Split the content into 2-3 sections
2. Process each section separately
3. Merge the resulting PPTX files manually
4. OR: Ask Gemini to generate in batches (Slides 1-20, 21-40, 41-58)

---

## After Gemini Processing

Once all weeks have PPTX files:

1. **Add speaker notes** to each week:
   ```
   /add-speaker-notes PPDK66B 1
   /add-speaker-notes PPDK66B 2
   ... etc.
   ```

2. **Verify output files** in each week's `output/slides.pptx`

3. **Check slide counts** match expected:
   - Week 1: 10 slides
   - Week 2: 28 slides
   - Week 3: 58 slides
   - Week 4: 30 slides
   - Week 5: 23 slides
   - Week 7: 22 slides
   - Week 8: 25 slides
   - Week 9: 10 slides
   - Week 11: 22 slides
   - Week 12: 27 slides

4. **Spot check video slides** (Weeks 1, 9):
   - Video links are clickable
   - Speaker photos/thumbnails present
   - Duration displayed clearly
   - Pre-viewing questions visible (Week 9 Dweck)

5. **Final deliverables location:**
   ```
   courses/PPDK66B-personal-professional-development/weeks/week-NN/output/slides.pptx
   ```

---

## Troubleshooting

### If Gemini condenses content:
```
"Reproduce the EXACT wording from the lecture content - do not summarize or paraphrase"
```
Generate one slide at a time for problematic sections.

### If images don't match:
```
"Use a photo of [specific scene]"
"Similar to [company name]'s branding"
```
Request regeneration of specific slide.

### If video slides missing elements:
```
"Add a prominent clickable video link"
"Include a professional photo of [speaker name]"
"Show duration clearly: [X] minutes"
```

### If Week 3 too long:
```
"Generate slides 1-20 first, then I'll request slides 21-40"
```
OR split content manually and process in batches.

---

## Quality Checklist (After All Weeks Complete)

- [ ] All 10 lecture weeks have slides.pptx in output/
- [ ] All PPTX files have speaker notes inserted
- [ ] Week 1 video link is clickable
- [ ] Week 9 Dweck video slide has pre-viewing question
- [ ] Week 9 Duckworth video is in "Further Resources" slide
- [ ] All slide counts match expected
- [ ] All slides have 4:3 aspect ratio
- [ ] Font sizes are readable (minimum 14pt)
- [ ] Citations in footers where appropriate
- [ ] Visual design is consistent across weeks

---

## Next Command After Gemini

Once all Gemini slides are downloaded and speaker notes added:

```
/package-course PPDK66B
```

This will:
- Convert all markdown to DOCX
- Package all deliverables
- Create final ZIP file for distribution

---

**Status:** Ready to begin Gemini processing
**Total estimated time:** 3-5 hours (depending on approach)
**Files ready:** 10 gemini-prompt.md files generated
