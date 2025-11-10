# Working Documents Management System

## Overview

This system keeps course directories clean by organizing temporary working documents, research files, and completed drafts into dedicated folders.

---

## Folder Structure

### Course-Level Organization

```
courses/[COURSE-CODE]/
├── .working/              # In-progress documents (hidden from main view)
│   ├── course-info.md
│   ├── progress-summary.md
│   ├── syllabus-DRAFT.md
│   └── research/
│       ├── course-description-research.md
│       ├── learning-objectives-research.md
│       └── article-research-summary.md
│
├── .archive/              # Completed documents for reference (hidden)
│   ├── [date]-course-info.md
│   ├── [date]-syllabus-DRAFT.md
│   └── [date]-COMPLETION-REPORT.md
│
├── syllabus.md           # FINAL published syllabus
├── assessments/          # Assessment schedules and prompts
├── rubrics/              # Grading rubrics
├── weeks/                # Weekly lecture and tutorial content
└── resources/            # Supporting materials
```

### Shared Research Organization

```
shared/research/
├── [course-topic]/
│   ├── article-research-summary.md
│   ├── course-description-research.md
│   └── learning-objectives-research.md
└── open-access-sources.md
```

---

## Document Categories

### **Working Documents** (`.working/`)

**Purpose:** In-progress files that support syllabus/content creation but aren't part of final deliverables.

**Contents:**
- `course-info.md` - Basic course metadata collected during setup
- `progress-summary.md` - Step-by-step progress tracking (for recovery if interrupted)
- `syllabus-DRAFT.md` - Draft syllabus built incrementally during article research
- `research/` subfolder:
  - `course-description-research.md` - Course description research from top schools
  - `learning-objectives-research.md` - Learning objectives research
  - `article-research-summary.md` - 4-stage article validation notes for all weeks

**Lifecycle:** Created during syllabus generation → Moved to `.archive/` when complete

---

### **Archive Documents** (`.archive/`)

**Purpose:** Completed working documents kept for reference, audit trail, or future course updates.

**Contents:**
- Timestamped copies of completed working documents
- Completion reports
- Previous syllabus versions (when updated)
- Research notes for major revisions

**Naming Convention:** `[YYYY-MM-DD]-[filename].md`

**Lifecycle:** Moved from `.working/` when course is complete or major milestone reached

---

### **Final Published Files** (Root level)

**Purpose:** The actual deliverables used by instructors and students.

**Contents:**
- `syllabus.md` - Final published syllabus
- `assessments/` - Assessment schedules and assignment prompts
- `rubrics/` - Grading rubrics extracted from syllabus
- `weeks/` - Lecture and tutorial content for each week
- `resources/` - Supporting materials (templates, examples, etc.)

**Lifecycle:** Permanent files that define the course

---

## Workflow Integration

### During Syllabus Generation (`/generate-syllabus`)

**Step 1: Course Basics**
- Create `.working/` folder
- Save `course-info.md` to `.working/`
- Save `course-description-research.md` to `.working/research/`

**Step 2: Learning Objectives**
- Update `.working/course-info.md`
- Save `learning-objectives-research.md` to `.working/research/`

**Step 3: Assessment Structure**
- Save `assessment-schedule.md` to `assessments/` (final location)
- Update `.working/course-info.md`

**Step 4: Article Research**
- Save `.working/syllabus-DRAFT.md` every 2-3 weeks
- Save `.working/research/article-research-summary.md` after each week
- Update `.working/progress-summary.md` continuously

**Step 5: Rubrics**
- Save rubrics to `rubrics/` (final location)
- Update `.working/syllabus-DRAFT.md`

**Step 6: Final Assembly**
- Save final `syllabus.md` to root (final location)
- Create `.working/COMPLETION-REPORT.md`
- Keep `.working/syllabus-DRAFT.md` for reference

---

### Archiving Completed Work (`/archive-course-work`)

**When to Archive:**
- Syllabus generation complete
- Course fully developed (all weeks generated)
- Major syllabus revision completed
- Academic year ends

**What Gets Archived:**
```bash
# Move working documents to archive with timestamps
.working/course-info.md           → .archive/[DATE]-course-info.md
.working/progress-summary.md      → .archive/[DATE]-progress-summary.md
.working/syllabus-DRAFT.md        → .archive/[DATE]-syllabus-DRAFT.md
.working/COMPLETION-REPORT.md     → .archive/[DATE]-COMPLETION-REPORT.md
.working/research/*               → .archive/research/[DATE]-*

# Clean up .working/ folder after archiving
```

**What Stays in `.working/`:**
- Empty folder structure (ready for next revision)
- OR: Keep current working docs if course updates ongoing

---

## Commands

### `/archive-course-work [COURSE-CODE]`

**Purpose:** Move completed working documents to archive with timestamps.

**Usage:**
```
/archive-course-work BCI2AU
```

**Actions:**
1. Create `.archive/` folder if doesn't exist
2. Add timestamp prefix to all files in `.working/`
3. Move files to `.archive/`
4. Create archive manifest listing what was archived and when
5. Clean `.working/` folder

**Safety:**
- Never overwrites existing archive files (adds `-2`, `-3` suffix if needed)
- Creates backup before moving
- Confirms action if syllabus not marked as complete

---

### `/clean-working-docs [COURSE-CODE]`

**Purpose:** Remove all working documents without archiving (use with caution).

**Usage:**
```
/clean-working-docs BCI2AU
```

**Actions:**
1. Verify final syllabus exists
2. Confirm with user before deletion
3. Remove `.working/` folder entirely
4. Log what was deleted

**Safety:**
- Requires confirmation
- Only works if `syllabus.md` exists
- Creates deletion log in `.archive/deletion-log.md`

---

## Best Practices

### **During Development**

1. **Let the generator save to `.working/`** - Don't manually move files during development
2. **Check `.working/progress-summary.md`** - If conversation interrupts, this shows where to resume
3. **Review `.working/syllabus-DRAFT.md`** - Validate incremental progress before finalizing
4. **Keep research in `.working/research/`** - Full audit trail of article validation decisions

### **After Completion**

1. **Archive working docs** - Run `/archive-course-work [CODE]` when syllabus complete
2. **Keep archive for reference** - Useful when updating course or creating similar courses
3. **Clean root directory** - Only final deliverables should be visible in main course folder
4. **Version control archive** - Git commit archive folder to track course evolution

### **For Updates**

1. **Copy from archive to working** - When revising syllabus, restore needed research docs
2. **Archive old syllabus** - Move current `syllabus.md` to `.archive/[DATE]-syllabus-v1.md`
3. **Document changes** - Create `.working/revision-notes.md` explaining updates
4. **Re-archive when complete** - New archive with timestamp for updated version

---

## File Retention Guidelines

### Keep Forever (Root Level)
- Final `syllabus.md`
- All `weeks/` content
- All `rubrics/`
- All `assessments/`

### Keep in Archive (Reference)
- Research summaries (useful for similar courses)
- Completion reports (audit trail)
- Progress summaries (recovery documentation)
- Draft syllabi (version history)

### Can Delete After 1 Year
- Course info metadata (if course not being updated)
- Progress tracking files (if course stable)

### Never Delete
- Article research summaries (expensive to regenerate)
- Learning objectives research (valuable for future courses)
- Course description research (reusable across years)

---

## Migration Guide

### Migrating Existing Courses

For courses created before this system:

```bash
# 1. Create folder structure
mkdir -p courses/[COURSE-CODE]/.working/research
mkdir -p courses/[COURSE-CODE]/.archive

# 2. Move working documents
mv courses/[COURSE-CODE]/course-info.md courses/[COURSE-CODE]/.working/
mv courses/[COURSE-CODE]/PROGRESS-SUMMARY.md courses/[COURSE-CODE]/.working/progress-summary.md
mv courses/[COURSE-CODE]/syllabus-DRAFT.md courses/[COURSE-CODE]/.working/

# 3. Move research documents
mv shared/research/[topic]/* courses/[COURSE-CODE]/.working/research/

# 4. Keep finals in root
# syllabus.md, assessments/, rubrics/, weeks/ stay where they are

# 5. Archive if complete
# Run /archive-course-work [COURSE-CODE]
```

---

## Technical Implementation Notes

### Hidden Folders

Using `.working/` and `.archive/` (with leading dot):
- ✅ Hidden from Finder by default on macOS/Linux
- ✅ Not indexed by most search tools
- ✅ Clear signal these are meta-files
- ✅ Standard Unix convention
- ⚠️ Visible in `ls -a` and editors (intentional - we need access)

### Generator Updates Required

**Files needing modification:**
- `.claude/commands/generate-syllabus.md` - Update all save paths to `.working/`
- `.claude/commands/new-course.md` - Create `.working/` and `.archive/` during setup
- `.claude/commands/generate-week.md` - Reference `.working/research/` for article info

**Backward compatibility:**
- Check if `.working/` exists; if not, create it
- Check old locations first, then new locations
- Provide migration instructions if old structure detected

---

## Example: BCI2AU Migration

### Current Structure
```
courses/BCI2AU-business-communication/
├── COMPLETION-REPORT.md
├── PROGRESS-SUMMARY.md
├── course-info.md
├── syllabus-DRAFT.md
├── syllabus.md
└── assessments/
    └── assessment-schedule.md

shared/research/business-communication-bci2au/
└── article-research-summary.md
```

### After Migration
```
courses/BCI2AU-business-communication/
├── .working/
│   ├── course-info.md
│   ├── progress-summary.md
│   ├── syllabus-DRAFT.md
│   ├── COMPLETION-REPORT.md
│   └── research/
│       └── article-research-summary.md
├── .archive/              # Empty until archived
├── syllabus.md           # FINAL (stays in root)
└── assessments/
    └── assessment-schedule.md
```

### After Archiving
```
courses/BCI2AU-business-communication/
├── .working/              # Empty (ready for future updates)
├── .archive/
│   ├── 2025-01-05-course-info.md
│   ├── 2025-01-05-progress-summary.md
│   ├── 2025-01-05-syllabus-DRAFT.md
│   ├── 2025-01-05-COMPLETION-REPORT.md
│   └── research/
│       └── 2025-01-05-article-research-summary.md
├── syllabus.md           # FINAL
└── assessments/
    └── assessment-schedule.md
```

---

## Summary

**Benefits of This System:**

1. ✅ **Clean root directories** - Only final deliverables visible
2. ✅ **Clear separation** - Working docs separate from published materials
3. ✅ **Audit trail** - Research and decisions documented in archive
4. ✅ **Recovery support** - Progress tracking enables conversation resumption
5. ✅ **Version history** - Archive maintains course evolution over time
6. ✅ **Reusability** - Research documents easily referenced for similar courses
7. ✅ **Standard conventions** - Hidden folders follow Unix/macOS conventions

**Two Approaches Supported:**

1. **Original creation in `.working/`** - Generator saves all working docs to `.working/` from start
2. **Move to `.archive/` when complete** - `/archive-course-work` command archives completed work

**Result:** Professional, maintainable course directory structure that scales across multiple courses and years.

---

**Last Updated:** January 5, 2025
**Version:** 1.0
