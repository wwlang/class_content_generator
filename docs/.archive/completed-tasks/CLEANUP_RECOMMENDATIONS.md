# Project Cleanup Recommendations

Analysis of redundant files and folders in class_content_generator project.

---

## 🗑️ RECOMMENDED DELETIONS

### 1. Temporary/System Files (DELETE IMMEDIATELY)

**High Priority - No value, should never be committed:**

- [ ] `__pycache__/` - Python compiled cache (auto-generated)
- [ ] `.DS_Store` - macOS system file (auto-generated)
- [ ] `.tmp.drivedownload/` - Google Drive temp folder (empty)
- [ ] `.tmp.driveupload/` - Google Drive temp folder (small temp files)

**Action:** Delete and add to `.gitignore`

```bash
rm -rf __pycache__ .DS_Store .tmp.drivedownload .tmp.driveupload
```

---

### 2. Generated Output Files (MOVE OR DELETE)

**Files that should be in .gitignore or moved to samples:**

- [ ] `enhanced-sample-slides.pptx` - Generated output file (44 KB)
  - **Recommendation:** Move to `samples/` OR delete and regenerate as needed

**Action:**
```bash
# Option 1: Move to samples
mv enhanced-sample-slides.pptx samples/

# Option 2: Delete (can regenerate)
rm enhanced-sample-slides.pptx
```

---

### 3. Test/Demo HTML Files (MOVE TO SAMPLES)

**Test files in root directory:**

- [ ] `showcase-enhancements.html` - Test HTML for converter (7 KB)
  - **Current location:** Root directory
  - **Better location:** `samples/` or `.claude/skills/slide-exporter/resources/examples/`
  - **Status:** Duplicate of existing sample files

**Action:**
```bash
# Check if duplicate
diff showcase-enhancements.html .claude/skills/slide-exporter/resources/examples/enhanced-sample-slides.html

# If duplicate, delete
rm showcase-enhancements.html

# If unique, move to samples
mv showcase-enhancements.html samples/
```

---

### 4. Empty/Unused Directories (DELETE)

**Directories with no content:**

- [ ] `resources/` - Only contains empty `icons/` subdirectory
  - **Status:** Completely empty, no files
  - **Recommendation:** Delete (can recreate if needed)

**Action:**
```bash
rm -rf resources/
```

---

### 5. Analysis/Development Scripts (MOVE TO TOOLS)

**One-off development tools:**

- [ ] `analyze_pptx_design.py` - PPTX analysis script (6 KB)
  - **Purpose:** Analyze PowerPoint design elements
  - **Usage:** Development/analysis tool
  - **Recommendation:** Move to `tools/` directory or delete if no longer needed

**Action:**
```bash
# Create tools directory
mkdir -p tools

# Move analysis script
mv analyze_pptx_design.py tools/

# Update .gitignore to exclude tools output
```

---

### 6. Redundant Documentation (REVIEW)

**Potentially overlapping documentation:**

- [ ] `UPDATES-SUMMARY.md` - System updates log (10 KB)
  - **Content:** Vietnamese ESL support, grading systems, article policy updates
  - **Status:** Historical changes from November 5, 2025
  - **Overlap:** Information may be integrated into `.claude/CLAUDE.md`
  - **Recommendation:**
    - Review if all info is in `.claude/CLAUDE.md`
    - If yes, move to `.archive/` or delete
    - If no, integrate into main docs, then archive

- [ ] `REFACTORING_PLAN.md` - 5-day refactoring plan (7 KB)
  - **Content:** Architectural refactoring roadmap
  - **Status:** Plan is now complete (Days 1-3 done)
  - **Recommendation:**
    - Move to `.archive/refactoring/` for historical reference
    - Core architectural info already in README

**Action:**
```bash
# Create archive directory
mkdir -p .archive/refactoring
mkdir -p .archive/historical-docs

# Move completed plans
mv REFACTORING_PLAN.md .archive/refactoring/
mv UPDATES-SUMMARY.md .archive/historical-docs/
```

---

### 7. Reference Documents (KEEP BUT ORGANIZE)

**Documents to keep but could be better organized:**

- ✅ `reference-design-style-guide.md` - Design guidelines (5 KB)
  - **Recommendation:** Move to `docs/` directory

- ✅ `lecture_content_instructions.md` - Content generation guide (12 KB)
  - **Recommendation:** Keep in root OR move to `docs/`

**Action:**
```bash
mkdir -p docs

# Option: Organize docs
mv reference-design-style-guide.md docs/
# mv lecture_content_instructions.md docs/  # Optional
```

---

## ✅ UPDATE .gitignore

**Add the following to `.gitignore`:**

```gitignore
# Temporary image cache
temp_images/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Google Drive temp
.tmp.driveupload/
.tmp.drivedownload/

# Generated outputs (optional - comment out if you want to track)
*.pptx
!samples/*.pptx

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.venv
venv/
ENV/

# Archives
.archive/
```

---

## 📁 RECOMMENDED NEW STRUCTURE

**After cleanup:**

```
class_content_generator/
├── .archive/              # NEW: Historical docs
│   ├── refactoring/
│   └── historical-docs/
│
├── .claude/               # Workflows and commands
│
├── docs/                  # NEW: Organized documentation
│   └── reference-design-style-guide.md
│
├── html_to_pptx/          # Converter package
│
├── tools/                 # NEW: Development utilities
│   └── analyze_pptx_design.py
│
├── samples/               # Sample files
│   ├── enhanced-sample-slides.pptx
│   └── BUSINESS COMMUNICATION Syllabus Fall 2025.md
│
├── courses/               # Generated courses
├── templates/             # Course templates
├── shared/                # Shared resources
│
├── html_to_pptx_converter.py  # Main converter
├── lecture_content_instructions.md
├── README.md
├── .gitignore            # UPDATED
└── .env.example
```

---

## 📊 CLEANUP SUMMARY

### Files to Delete (7 items):
1. `__pycache__/` directory
2. `.DS_Store` file
3. `.tmp.drivedownload/` directory
4. `.tmp.driveupload/` directory
5. `resources/` directory (empty)
6. `showcase-enhancements.html` (if duplicate)
7. `enhanced-sample-slides.pptx` (or move to samples)

### Files to Archive (2 items):
1. `REFACTORING_PLAN.md` → `.archive/refactoring/`
2. `UPDATES-SUMMARY.md` → `.archive/historical-docs/`

### Files to Move (3 items):
1. `analyze_pptx_design.py` → `tools/`
2. `reference-design-style-guide.md` → `docs/`
3. `enhanced-sample-slides.pptx` → `samples/` (optional)

### .gitignore Updates:
- Add 20+ patterns for Python, macOS, IDEs, generated files

**Total Space Reclaimed:** ~60 KB (not significant, but cleaner structure)
**Main Benefit:** Cleaner repository, professional organization, clear separation of concerns

---

## 🚀 AUTOMATED CLEANUP SCRIPT

```bash
#!/bin/bash
# cleanup.sh - Automated project cleanup

echo "🧹 Starting project cleanup..."

# 1. Delete temporary/system files
echo "Deleting temporary files..."
rm -rf __pycache__
rm -f .DS_Store
rm -rf .tmp.drivedownload .tmp.driveupload

# 2. Delete empty directories
echo "Removing empty directories..."
rm -rf resources/

# 3. Create new directory structure
echo "Creating directory structure..."
mkdir -p .archive/refactoring
mkdir -p .archive/historical-docs
mkdir -p docs
mkdir -p tools

# 4. Move files to appropriate locations
echo "Organizing files..."
mv REFACTORING_PLAN.md .archive/refactoring/ 2>/dev/null || true
mv UPDATES-SUMMARY.md .archive/historical-docs/ 2>/dev/null || true
mv analyze_pptx_design.py tools/ 2>/dev/null || true
mv reference-design-style-guide.md docs/ 2>/dev/null || true

# 5. Move or delete generated outputs
if [ -f enhanced-sample-slides.pptx ]; then
    echo "Moving generated PPTX to samples..."
    mv enhanced-sample-slides.pptx samples/
fi

if [ -f showcase-enhancements.html ]; then
    # Check if it's a duplicate
    if diff -q showcase-enhancements.html .claude/skills/slide-exporter/resources/examples/enhanced-sample-slides.html >/dev/null 2>&1; then
        echo "Removing duplicate HTML file..."
        rm showcase-enhancements.html
    else
        echo "Moving unique HTML to samples..."
        mv showcase-enhancements.html samples/
    fi
fi

echo "✅ Cleanup complete!"
echo ""
echo "Don't forget to update .gitignore with recommended patterns!"
```

**To run:**
```bash
chmod +x cleanup.sh
./cleanup.sh
```

---

## ⚠️ BEFORE RUNNING CLEANUP

1. **Backup important files** (if any doubt)
2. **Review UPDATES-SUMMARY.md** - Ensure all info is captured elsewhere
3. **Check analyze_pptx_design.py** - Confirm not needed for production
4. **Verify showcase-enhancements.html** - Check if duplicate
5. **Commit current state** to git (if using version control)

---

**Created:** 2025-11-10
**Purpose:** Organize project structure and remove redundant files
**Impact:** Cleaner repository, better organization, professional structure
