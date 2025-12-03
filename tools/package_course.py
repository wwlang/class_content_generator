#!/usr/bin/env python3
"""
Package course materials into deliverable ZIP archive.

Collects all deliverable files (.docx, .pptx, .gift) from a course directory
and creates a ZIP archive preserving the relative folder structure.

Usage:
    python tools/package_course.py [course-code]
    python tools/package_course.py [course-code] --base-path [path]

Example:
    python tools/package_course.py BCI2AU
    python tools/package_course.py BCI2AU --base-path /path/to/courses
"""

import os
import sys
import glob
import zipfile
import argparse
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Import markdown_to_docx converter functions
try:
    # Try relative import first (when imported as module)
    from tools.markdown_to_docx import (
        convert_syllabus,
        convert_handbook,
        convert_tutor_guide,
        convert_package_guide,
        convert_assessment_file
    )
    CONVERTER_AVAILABLE = True
except ImportError:
    try:
        # Try absolute import (when run as script)
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from tools.markdown_to_docx import (
            convert_syllabus,
            convert_handbook,
            convert_tutor_guide,
            convert_package_guide,
            convert_assessment_file
        )
        CONVERTER_AVAILABLE = True
    except ImportError:
        CONVERTER_AVAILABLE = False


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class PackageReport:
    """Result of packaging operation."""
    success: bool
    package_path: str
    files_collected: int
    files_by_category: Dict[str, int]
    output_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# =============================================================================
# COURSE PATH FUNCTIONS
# =============================================================================

def find_course_path(course_code: str, base_path: Optional[str] = None) -> str:
    """
    Locate course directory by code.

    Args:
        course_code: Course code (e.g., "BCI2AU")
        base_path: Optional base directory (defaults to project root)

    Returns:
        Absolute path to course directory

    Raises:
        FileNotFoundError: If course directory not found
    """
    if base_path is None:
        # Default: assume script is in tools/, navigate to project root
        script_dir = Path(__file__).parent
        base_path = script_dir.parent / "courses"
    else:
        base_path = Path(base_path)

    # Find course folder (format: CODE-name or just CODE)
    course_pattern = os.path.join(base_path, f"{course_code}*")
    matches = glob.glob(course_pattern)

    if not matches:
        raise FileNotFoundError(
            f"Course not found: {course_code} in {base_path}"
        )

    if len(matches) > 1:
        raise ValueError(
            f"Multiple courses found for {course_code}: {matches}"
        )

    course_path = matches[0]

    if not os.path.isdir(course_path):
        raise FileNotFoundError(
            f"Course path is not a directory: {course_path}"
        )

    return course_path


# =============================================================================
# FILE COLLECTION FUNCTIONS
# =============================================================================

def collect_deliverable_files(course_path: str) -> Dict[str, List[str]]:
    """
    Collect all deliverable files from course directory.

    Collects .docx, .pptx, and .gift files from:
    - output/: syllabus.docx, assessment-handbook.docx
    - root: tutor-guide.docx
    - package/: README.docx
    - assessments/output/: assessment briefs and consolidated quiz
    - weeks/week-*/output/: tutorial materials and week quizzes

    Args:
        course_path: Absolute path to course directory

    Returns:
        Dictionary organized by category:
        {
            'root': [file_paths],
            'assessments': [file_paths],
            'weeks': {
                'week-01': [file_paths],
                'week-02': [file_paths],
                ...
            }
        }
    """
    files = {
        'root': [],
        'assessments': [],
        'weeks': {}
    }

    # Root level output folder: syllabus and assessment handbook
    root_output_dir = os.path.join(course_path, 'output')
    if os.path.exists(root_output_dir):
        for filename in ['syllabus.docx', 'assessment-handbook.docx']:
            file_path = os.path.join(root_output_dir, filename)
            if os.path.exists(file_path):
                files['root'].append(file_path)

    # Course root: tutor guide
    tutor_guide = os.path.join(course_path, 'tutor-guide.docx')
    if os.path.exists(tutor_guide):
        files['root'].append(tutor_guide)

    # Package folder: README.docx (course package guide)
    readme_path = os.path.join(course_path, 'package', 'README.docx')
    if os.path.exists(readme_path):
        files['root'].append(readme_path)

    # Assessments output folder: all .docx and .gift files
    assessments_output_dir = os.path.join(course_path, 'assessments', 'output')
    if os.path.exists(assessments_output_dir):
        # Collect DOCX files (assessment briefs), excluding Word temp files (~$*)
        docx_files = glob.glob(os.path.join(assessments_output_dir, '*.docx'))
        docx_files = [f for f in docx_files if not os.path.basename(f).startswith('~$')]
        files['assessments'].extend(docx_files)

        # Collect GIFT files (consolidated quizzes)
        gift_files = glob.glob(os.path.join(assessments_output_dir, '*.gift'))
        files['assessments'].extend(gift_files)

    # Weeks: output folder contents
    weeks_pattern = os.path.join(course_path, 'weeks', 'week-*')
    week_dirs = sorted(glob.glob(weeks_pattern))

    for week_dir in week_dirs:
        week_name = os.path.basename(week_dir)
        output_dir = os.path.join(week_dir, 'output')

        if not os.path.exists(output_dir):
            continue

        week_files = []

        # Collect DOCX files (tutorial materials), excluding Word temp files (~$*)
        docx_files = glob.glob(os.path.join(output_dir, '*.docx'))
        docx_files = [f for f in docx_files if not os.path.basename(f).startswith('~$')]
        week_files.extend(docx_files)

        # Collect PPTX files (lecture slides), excluding temp files (~$*)
        pptx_files = glob.glob(os.path.join(output_dir, '*.pptx'))
        pptx_files = [f for f in pptx_files if not os.path.basename(f).startswith('~$')]
        week_files.extend(pptx_files)

        # Collect GIFT files (week quizzes)
        gift_files = glob.glob(os.path.join(output_dir, '*.gift'))
        week_files.extend(gift_files)

        # Collect readings folder if it exists
        readings_dir = os.path.join(output_dir, 'readings')
        if os.path.exists(readings_dir):
            # Add all files from readings folder, excluding temp files (~$*)
            reading_files = glob.glob(os.path.join(readings_dir, '*'))
            for reading_file in reading_files:
                if os.path.isfile(reading_file) and not os.path.basename(reading_file).startswith('~$'):
                    week_files.append(reading_file)

        if week_files:
            files['weeks'][week_name] = sorted(week_files)

    return files


def count_files_by_type(files_dict: Dict) -> Dict[str, int]:
    """
    Count files by category for reporting.

    Args:
        files_dict: File collection from collect_deliverable_files()

    Returns:
        Count dictionary: {'root': N, 'assessments': N, 'weeks': N, 'total': N}
    """
    counts = {
        'root': len(files_dict['root']),
        'assessments': len(files_dict['assessments']),
        'weeks': sum(len(week_files) for week_files in files_dict['weeks'].values()),
    }
    counts['total'] = sum(counts.values())

    return counts


# =============================================================================
# ZIP ARCHIVE FUNCTIONS
# =============================================================================

def create_package_zip(
    course_code: str,
    files_dict: Dict,
    course_path: str,
    output_dir: str
) -> str:
    """
    Create ZIP archive with preserved folder structure.

    ZIP structure:
        syllabus.docx
        assessment-handbook.docx
        tutor-guide.docx
        README.docx
        assessments/
            brief1.docx
            brief2.docx
            consolidated-quiz.gift
        weeks/
            week-01/
                tutorial-content.docx
                tutorial-tutor-notes.docx
                slides.pptx
                week-01-quiz.gift
            week-02/
                ...

    Args:
        course_code: Course code for ZIP filename
        files_dict: File collection from collect_deliverable_files()
        course_path: Absolute path to course directory
        output_dir: Directory to create ZIP file in

    Returns:
        Absolute path to created ZIP file
    """
    # Create package directory
    os.makedirs(output_dir, exist_ok=True)

    # ZIP filename
    zip_filename = f'{course_code}-deliverables.zip'
    zip_path = os.path.join(output_dir, zip_filename)

    # Remove existing ZIP file if it exists (ensure clean overwrite)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    # Create ZIP archive
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add root files
        for file_path in files_dict['root']:
            arcname = os.path.basename(file_path)
            zf.write(file_path, arcname)

        # Add assessment files
        for file_path in files_dict['assessments']:
            arcname = os.path.join('assessments', os.path.basename(file_path))
            zf.write(file_path, arcname)

        # Add week files
        for week_name, week_files in sorted(files_dict['weeks'].items()):
            for file_path in week_files:
                # Check if file is in readings subfolder
                if 'readings' in file_path:
                    # Preserve readings subfolder structure: weeks/week-01/readings/file.pdf
                    relative_to_output = os.path.relpath(
                        file_path,
                        os.path.join(course_path, 'weeks', week_name, 'output')
                    )
                    arcname = os.path.join('weeks', week_name, relative_to_output)
                else:
                    # Regular file: weeks/week-01/filename.ext
                    arcname = os.path.join('weeks', week_name, os.path.basename(file_path))
                zf.write(file_path, arcname)

    return zip_path


# =============================================================================
# GUIDE GENERATION
# =============================================================================

def generate_package_guide(course_code: str, course_path: str) -> None:
    """
    Generate course-package-guide.md from template if it doesn't exist.

    Args:
        course_code: Course code
        course_path: Path to course directory
    """
    guide_path = os.path.join(course_path, 'package', 'course-package-guide.md')

    # Skip if guide already exists
    if os.path.exists(guide_path):
        return

    # Load template
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'templates',
        'course-package-guide.md'
    )

    if not os.path.exists(template_path):
        print(f"Warning: Template not found at {template_path}")
        return

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Extract course info
    from tools.markdown_to_docx import extract_course_info
    course_info = extract_course_info(course_path)

    if not course_info:
        course_name = "Course"
        total_weeks = "10"
    else:
        course_name = course_info.name
        # Try to count weeks
        weeks_pattern = os.path.join(course_path, 'weeks', 'week-*')
        week_dirs = glob.glob(weeks_pattern)
        total_weeks = str(len(week_dirs)) if week_dirs else "10"

    # Fill template
    guide_content = template.format(
        course_code=course_code,
        course_name=course_name,
        total_weeks=total_weeks
    )

    # Create package directory
    os.makedirs(os.path.dirname(guide_path), exist_ok=True)

    # Write guide
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)

    print(f"Generated course-package-guide.md")


# =============================================================================
# CONVERSION FUNCTIONS
# =============================================================================

def ensure_docx_conversions(course_code: str, course_path: str) -> List[str]:
    """
    Convert all markdown files to DOCX before packaging.

    Always converts (overwrites existing DOCX):
    - syllabus.md → output/syllabus.docx
    - assessment-handbook.md → output/assessment-handbook.docx
    - tutor-guide.md → tutor-guide.docx
    - package/course-package-guide.md → package/README.docx

    Returns:
        List of warnings if conversions failed
    """
    warnings = []

    if not CONVERTER_AVAILABLE:
        warnings.append("Markdown converter not available - skipping conversions")
        return warnings

    conversions = [
        ('syllabus', 'syllabus.md', 'output/syllabus.docx'),
        ('handbook', 'assessment-handbook.md', 'output/assessment-handbook.docx'),
        ('tutor-guide', 'tutor-guide.md', 'tutor-guide.docx'),
        ('guide', 'package/course-package-guide.md', 'package/README.docx'),
    ]

    for conv_type, md_file, docx_file in conversions:
        md_path = os.path.join(course_path, md_file)

        # Skip if markdown doesn't exist
        if not os.path.exists(md_path):
            continue

        # Always convert
        print(f"Converting {md_file} → {docx_file}...")
        try:
            if conv_type == 'syllabus':
                convert_syllabus(course_code)
            elif conv_type == 'handbook':
                convert_handbook(course_code)
            elif conv_type == 'tutor-guide':
                convert_tutor_guide(course_code)
            elif conv_type == 'guide':
                convert_package_guide(course_code)
        except Exception as e:
            warnings.append(f"Failed to convert {md_file}: {str(e)}")

    # Convert assessment markdown files
    assessments_folder = os.path.join(course_path, 'assessments')
    if os.path.exists(assessments_folder):
        assessment_md_files = glob.glob(os.path.join(assessments_folder, '*.md'))
        for md_path in assessment_md_files:
            filename = os.path.basename(md_path)
            # Skip assessment-schedule.md (internal reference only)
            if filename == 'assessment-schedule.md':
                continue
            print(f"Converting assessments/{filename}...")
            try:
                convert_assessment_file(course_code, filename)
            except Exception as e:
                warnings.append(f"Failed to convert {filename}: {str(e)}")

    return warnings


# =============================================================================
# MAIN PACKAGING FUNCTION
# =============================================================================

def package_course(
    course_code: str,
    base_path: Optional[str] = None
) -> PackageReport:
    """
    Main packaging orchestration function.

    Args:
        course_code: Course code (e.g., "BCI2AU")
        base_path: Optional base directory for courses

    Returns:
        PackageReport with results
    """
    errors = []
    warnings = []
    output_files = []

    try:
        # 1. Find course directory
        course_path = find_course_path(course_code, base_path)

        # 2. Generate package guide if needed
        generate_package_guide(course_code, course_path)

        # 3. Ensure all DOCX conversions are up-to-date
        conversion_warnings = ensure_docx_conversions(course_code, course_path)
        warnings.extend(conversion_warnings)

        # 4. Collect deliverable files
        files_dict = collect_deliverable_files(course_path)

        # 5. Validate we have files to package
        file_counts = count_files_by_type(files_dict)

        if file_counts['total'] == 0:
            errors.append("No deliverable files found to package")
            return PackageReport(
                success=False,
                package_path="",
                files_collected=0,
                files_by_category=file_counts,
                output_files=[],
                errors=errors,
                warnings=warnings
            )

        # 6. Create package directory
        package_dir = os.path.join(course_path, 'package')

        # 7. Create ZIP archive
        zip_path = create_package_zip(
            course_code,
            files_dict,
            course_path,
            package_dir
        )

        output_files.append(zip_path)

        # 8. Add warnings for missing expected files
        if file_counts['root'] == 0:
            warnings.append("No root files (syllabus, handbook) found")

        if file_counts['assessments'] == 0:
            warnings.append("No assessment files found")

        if file_counts['weeks'] == 0:
            warnings.append("No week output files found")

        # 9. Return success report
        return PackageReport(
            success=True,
            package_path=zip_path,
            files_collected=file_counts['total'],
            files_by_category=file_counts,
            output_files=output_files,
            errors=[],
            warnings=warnings
        )

    except FileNotFoundError as e:
        errors.append(str(e))
        return PackageReport(
            success=False,
            package_path="",
            files_collected=0,
            files_by_category={},
            output_files=[],
            errors=errors,
            warnings=warnings
        )

    except Exception as e:
        errors.append(f"Unexpected error: {str(e)}")
        return PackageReport(
            success=False,
            package_path="",
            files_collected=0,
            files_by_category={},
            output_files=[],
            errors=errors,
            warnings=warnings
        )


# =============================================================================
# REPORTING FUNCTIONS
# =============================================================================

def print_report(report: PackageReport) -> None:
    """
    Display packaging results to user.

    Args:
        report: PackageReport from package_course()
    """
    print("\n" + "=" * 60)
    print("COURSE PACKAGING REPORT")
    print("=" * 60)

    if report.success:
        print(f"✓ Packaging successful")
        print(f"\nPackage created:")
        print(f"  {report.package_path}")

        print(f"\nFiles packaged: {report.files_collected}")

        if report.files_by_category:
            print(f"\nBreakdown by category:")
            if report.files_by_category.get('root', 0) > 0:
                print(f"  - Root files:       {report.files_by_category['root']}")
            if report.files_by_category.get('assessments', 0) > 0:
                print(f"  - Assessment files: {report.files_by_category['assessments']}")
            if report.files_by_category.get('weeks', 0) > 0:
                print(f"  - Week files:       {report.files_by_category['weeks']}")

        if report.warnings:
            print(f"\nWarnings:")
            for warning in report.warnings:
                print(f"  ⚠ {warning}")

    else:
        print(f"✗ Packaging failed")

        if report.errors:
            print(f"\nErrors:")
            for error in report.errors:
                print(f"  ✗ {error}")

    print("=" * 60 + "\n")


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main():
    """Command-line interface for course packaging."""
    parser = argparse.ArgumentParser(
        description="Package course deliverables into ZIP archive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/package_course.py BCI2AU
  python tools/package_course.py BCI2AU --base-path /path/to/courses
        """
    )

    parser.add_argument(
        'course_code',
        help='Course code (e.g., BCI2AU)'
    )

    parser.add_argument(
        '--base-path',
        help='Base path to courses directory (optional)'
    )

    args = parser.parse_args()

    # Run packaging
    report = package_course(args.course_code, args.base_path)

    # Display report
    print_report(report)

    # Exit with appropriate code
    return 0 if report.success else 1


if __name__ == '__main__':
    sys.exit(main())
