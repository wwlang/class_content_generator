# Font Embedding in PPTX Files

## Current Status: IMPLEMENTED ✓

The project includes a **dedicated font embedding tool** (`tools/embed_fonts_in_pptx.py`) that embeds Cal Sans and Plus Jakarta Sans fonts into PPTX files after conversion.

## Quick Usage

### Two-Step Workflow

```bash
# Step 1: Generate PPTX from HTML
python3 html_to_pptx_converter.py input.html output.pptx

# Step 2: Embed fonts
python3 tools/embed_fonts_in_pptx.py output.pptx
```

**That's it!** The output PPTX now has fonts embedded and will display correctly on any computer.

## Why This Matters

**Fonts Used:**
- **Cal Sans** (headers, titles) - Custom font
- **Plus Jakarta Sans** (body text) - Google Font

**Without font embedding:**
- PPTX opened on computers without these fonts will substitute Arial/Calibri
- Design changes significantly
- Professional appearance lost

**With font embedding:**
- ✓ Fonts display correctly on any computer
- ✓ Professional design preserved
- ✓ No installation required on recipient computers

## How It Works

The font embedding tool (`tools/embed_fonts_in_pptx.py`):

1. **Creates a backup** (`.pptx.backup`)
2. **Extracts PPTX** (PPTX is a ZIP archive)
3. **Copies font files** to `ppt/fonts/` directory
4. **Updates [Content_Types].xml** to register TTF files
5. **Repackages** everything as PPTX
6. **Reports** file size increase

### Font File Locations

The tool looks for fonts at:

```python
FONTS = {
    'Cal Sans': '/Users/williamlang/Library/Fonts/CalSans-Regular.ttf',
    'Plus Jakarta Sans': '/Users/williamlang/Library/Fonts/PlusJakartaSans-VariableFont_wght.ttf',
}
```

**Note:** Font paths are currently hardcoded to the developer's system. To use on other systems, update the paths in `tools/embed_fonts_in_pptx.py` (lines 19-22).

## Letter-Spacing Configuration

The converter properly applies **condensed letter-spacing** (`-0.05em`) to Cal Sans titles:

```python
# html_to_pptx/config.py (line 125)
TITLE_LETTER_SPACING = Pt(-0.65)  # Condensed by ~0.05em
```

This value is correctly applied in the PPTX via XML manipulation:

```python
# Applied in multiple handlers
spacing_hundredths = int(FontConfig.TITLE_LETTER_SPACING.pt * 100)
run.font._element.set('spc', str(spacing_hundredths))
```

**Result:** Letter-spacing is `-0.05em` with **no doubling or compounding**.

## Example Output

```bash
$ python3 tools/embed_fonts_in_pptx.py samples/comprehensive-layout-showcase.pptx

Processing: samples/comprehensive-layout-showcase.pptx
  ✓ Created backup: samples/comprehensive-layout-showcase.pptx.backup
  ✓ Extracted PPTX to temp directory
  ✓ Copied font: Cal Sans
  ✓ Copied font: Plus Jakarta Sans
  ✓ Updated [Content_Types].xml
  ✓ Repackaged PPTX with embedded fonts

✓ Font embedding complete!
  Original size: 62,417 bytes
  New size: 819,204 bytes (+756,787 bytes)
  Fonts embedded: 2
    - Cal Sans
    - Plus Jakarta Sans

Note: Font embedding in PowerPoint has limitations:
  - Variable fonts may not be fully supported
  - Some systems may not recognize embedded fonts
  - Fallback fonts (Arial Black, Arial) will be used if embedding fails
```

## File Size Impact

Typical file size increases:

| Font | Size Added |
|------|------------|
| Cal Sans (Regular) | ~500 KB |
| Plus Jakarta Sans (Variable) | ~300 KB |
| **Total Increase** | ~800 KB |

**Example:**
- Without fonts: 60 KB (25 slides)
- With fonts: 820 KB (25 slides)

**Trade-off:** Larger file size for guaranteed correct display everywhere.

## Font Licensing

**Before distributing embedded fonts, verify licenses:**

- **Plus Jakarta Sans:** Open Font License (OFL) - ✓ Embedding allowed
- **Cal Sans:** Check license with vendor - may have restrictions

The embedding tool includes fonts in the PPTX file, which counts as distribution. Ensure font licenses permit embedding and redistribution.

## Limitations & Notes

### Known Limitations

1. **Variable Font Support:**
   - Plus Jakarta Sans is a variable font
   - Some older PowerPoint versions may not fully support variable fonts
   - Fallback to system fonts occurs if not supported

2. **Font Paths:**
   - Hardcoded to developer's Mac system paths
   - Must be updated for Windows/Linux or other user accounts

3. **Backup Creation:**
   - Tool creates `.pptx.backup` files
   - Remember to clean up backups after verification

### Troubleshooting

**"Font not found" error:**
```bash
⚠ Font not found: Cal Sans (/Users/williamlang/Library/Fonts/CalSans-Regular.ttf)
```

**Solution:** Update font paths in `tools/embed_fonts_in_pptx.py` lines 19-22 to match your system.

**Variable font not displaying correctly:**
- Some PowerPoint versions don't fully support variable fonts
- Consider using static font files instead
- Or accept that fallback fonts will be used

## Making Font Paths Configurable

### Current (Hardcoded)

```python
# tools/embed_fonts_in_pptx.py
FONTS = {
    'Cal Sans': '/Users/williamlang/Library/Fonts/CalSans-Regular.ttf',
    'Plus Jakarta Sans': '/Users/williamlang/Library/Fonts/PlusJakartaSans-VariableFont_wght.ttf',
}
```

### Recommended Improvement (Configuration File)

Create `fonts.json` in project root:

```json
{
  "Cal Sans": "/path/to/CalSans-Regular.ttf",
  "Plus Jakarta Sans": "/path/to/PlusJakartaSans-VariableFont_wght.ttf"
}
```

Then update tool to read from config:

```python
import json

# Load font paths from config
with open('fonts.json', 'r') as f:
    FONTS = json.load(f)
```

This makes it easy for other users to configure without editing code.

## Alternative: PDF Export

If font embedding is problematic, convert to PDF instead:

```bash
# Generate PPTX first
python3 html_to_pptx_converter.py input.html output.pptx

# Convert to PDF (requires LibreOffice)
soffice --headless --convert-to pdf output.pptx
```

**PDF benefits:**
- ✓ Fonts always preserved (embedded automatically)
- ✓ Universal compatibility
- ✓ Smaller file size than embedded fonts

**PDF limitations:**
- ✗ Not editable
- ✗ No presenter notes visible during presentation

## Integration with Converter

### Automated Font Embedding (Future Enhancement)

Add `--embed-fonts` flag to main converter:

```bash
python3 html_to_pptx_converter.py input.html output.pptx --embed-fonts
```

**Implementation approach:**

```python
# In html_to_pptx_converter.py main()
def main():
    # ... parse arguments ...

    converter = HTMLToPPTXConverter()
    converter.convert(input_file, output_file)

    # Embed fonts if requested
    if embed_fonts:
        from tools.embed_fonts_in_pptx import embed_fonts_in_pptx
        embed_fonts_in_pptx(output_file)
```

This would make font embedding seamless and part of the standard workflow.

## Complete Workflow Example

### Standard Workflow (With Font Embedding)

```bash
# 1. Generate lecture content (creates markdown)
/generate-week 3

# 2. Convert to HTML (done by exporter skill)
# This step is automated

# 3. Convert to PPTX
python3 html_to_pptx_converter.py \
  courses/BUS101/weeks/week-3/slides.html \
  courses/BUS101/weeks/week-3/lecture-week-3.pptx

# 4. Embed fonts
python3 tools/embed_fonts_in_pptx.py \
  courses/BUS101/weeks/week-3/lecture-week-3.pptx

# 5. Ready to distribute!
# File now has fonts embedded and displays correctly everywhere
```

### Quick One-Liner (Bash)

```bash
# Generate and embed in one command
python3 html_to_pptx_converter.py input.html output.pptx && \
python3 tools/embed_fonts_in_pptx.py output.pptx && \
echo "✓ PPTX with embedded fonts ready!"
```

## Summary

| Aspect | Status |
|--------|--------|
| **Font embedding tool** | ✓ Implemented (`tools/embed_fonts_in_pptx.py`) |
| **Fonts supported** | Cal Sans, Plus Jakarta Sans |
| **Letter-spacing** | ✓ Correct (-0.05em, no doubling) |
| **File size increase** | ~800 KB per PPTX |
| **Automation** | Manual (run after conversion) |
| **Cross-platform** | Requires font path configuration |

**Recommended workflow:** Always run font embedding tool after PPTX generation before distributing files.

## Related Documentation

- **Font Configuration:** `html_to_pptx/config.py` (lines 80-126)
- **Converter Architecture:** `docs/ARCHITECTURE.md`
- **Validation Guide:** `docs/VALIDATION-GUIDE.md`

## Quick Reference

```bash
# Standard workflow
python3 html_to_pptx_converter.py input.html output.pptx
python3 tools/embed_fonts_in_pptx.py output.pptx

# Check what happened
ls -lh output.pptx*
# output.pptx         (with fonts, ~800KB larger)
# output.pptx.backup  (original without fonts)

# Verify fonts embedded
unzip -l output.pptx | grep fonts
# Should show:
#   ppt/fonts/CalSans-Regular.ttf
#   ppt/fonts/PlusJakartaSans-VariableFont_wght.ttf
```

---

**Last Updated:** January 11, 2025
**Status:** Font embedding fully implemented and working
**Tool Location:** `tools/embed_fonts_in_pptx.py`
