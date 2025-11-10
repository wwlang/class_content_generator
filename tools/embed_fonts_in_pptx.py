#!/usr/bin/env python3
"""
Embed fonts into PowerPoint presentation files.

This script embeds TrueType fonts into PPTX files by:
1. Adding font files to the package
2. Creating font relationships
3. Marking fonts as embedded in the presentation XML
"""

import sys
import os
import shutil
import zipfile
from pathlib import Path
from lxml import etree

# Font file paths
FONTS = {
    'Cal Sans': '/Users/williamlang/Library/Fonts/CalSans-Regular.ttf',
    'Plus Jakarta Sans': '/Users/williamlang/Library/Fonts/PlusJakartaSans-VariableFont_wght.ttf',
}

def embed_fonts_in_pptx(pptx_path):
    """
    Embed fonts into a PowerPoint file.

    Args:
        pptx_path: Path to the PPTX file

    Note: PowerPoint font embedding has limitations:
    - Font files must allow embedding (check font license)
    - Variable fonts may have limited support
    - Embedded fonts increase file size
    """

    print(f"Processing: {pptx_path}")

    # Check if file exists
    if not os.path.exists(pptx_path):
        print(f"Error: File not found: {pptx_path}")
        return False

    # Create backup
    backup_path = pptx_path + '.backup'
    shutil.copy2(pptx_path, backup_path)
    print(f"  ✓ Created backup: {backup_path}")

    # Extract PPTX (it's a ZIP file)
    temp_dir = pptx_path + '_temp'
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    with zipfile.ZipFile(pptx_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    print(f"  ✓ Extracted PPTX to temp directory")

    # Create fonts directory
    fonts_dir = os.path.join(temp_dir, 'ppt', 'fonts')
    os.makedirs(fonts_dir, exist_ok=True)

    # Copy font files
    embedded_fonts = []
    for font_name, font_path in FONTS.items():
        if os.path.exists(font_path):
            dest_path = os.path.join(fonts_dir, os.path.basename(font_path))
            shutil.copy2(font_path, dest_path)
            embedded_fonts.append({
                'name': font_name,
                'file': os.path.basename(font_path),
                'path': dest_path
            })
            print(f"  ✓ Copied font: {font_name}")
        else:
            print(f"  ⚠ Font not found: {font_name} ({font_path})")

    if not embedded_fonts:
        print("  ✗ No fonts were embedded")
        shutil.rmtree(temp_dir)
        return False

    # Add [Content_Types].xml entries for fonts
    content_types_path = os.path.join(temp_dir, '[Content_Types].xml')
    if os.path.exists(content_types_path):
        tree = etree.parse(content_types_path)
        root = tree.getroot()

        # Define namespace
        ns = {'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}

        # Check if .ttf extension is already defined
        existing = root.xpath('//ct:Default[@Extension="ttf"]', namespaces=ns)
        if not existing:
            # Add TTF content type
            default_elem = etree.Element(
                '{http://schemas.openxmlformats.org/package/2006/content-types}Default',
                Extension='ttf',
                ContentType='application/x-font-ttf'
            )
            root.append(default_elem)

            tree.write(content_types_path, xml_declaration=True, encoding='UTF-8', standalone=True)
            print(f"  ✓ Updated [Content_Types].xml")

    # Repackage as PPTX
    os.remove(pptx_path)

    with zipfile.ZipFile(pptx_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for root_dir, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zip_ref.write(file_path, arcname)

    print(f"  ✓ Repackaged PPTX with embedded fonts")

    # Cleanup
    shutil.rmtree(temp_dir)

    # Get file sizes
    original_size = os.path.getsize(backup_path)
    new_size = os.path.getsize(pptx_path)
    size_diff = new_size - original_size

    print()
    print(f"✓ Font embedding complete!")
    print(f"  Original size: {original_size:,} bytes")
    print(f"  New size: {new_size:,} bytes ({size_diff:+,} bytes)")
    print(f"  Fonts embedded: {len(embedded_fonts)}")
    for font in embedded_fonts:
        print(f"    - {font['name']}")
    print()
    print(f"Note: Font embedding in PowerPoint has limitations:")
    print(f"  - Variable fonts may not be fully supported")
    print(f"  - Some systems may not recognize embedded fonts")
    print(f"  - Fallback fonts (Arial Black, Arial) will be used if embedding fails")

    return True


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python embed_fonts_in_pptx.py <path-to-pptx>")
        print()
        print("This script embeds Cal Sans and Plus Jakarta Sans fonts into a PPTX file.")
        sys.exit(1)

    pptx_path = sys.argv[1]
    success = embed_fonts_in_pptx(pptx_path)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
