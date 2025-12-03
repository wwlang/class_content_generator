#!/usr/bin/env python3
"""
Download Reading Materials for Weekly Content.

Multi-source downloader that attempts to fetch academic articles from:
1. Direct URLs (open access PDFs)
2. Unpaywall API (legal open-access versions via DOI)
3. Fallback to reading list with institutional access instructions

Features:
- Smart PDF validation (checks magic bytes)
- Rate limiting to avoid blocking
- Clear source attribution
- Generates reading lists for manual institutional access

Note: Institutional proxy/authentication (EZproxy, Shibboleth) is NOT supported.
These systems require interactive login and 2FA. For paywalled articles, use
manual download workflow documented in docs/MANUAL-READING-DOWNLOAD.md

Usage:
    python tools/download_readings.py [course-code] [week-number]

Example:
    python tools/download_readings.py BCI2AU 1

Expected Success Rate:
    - Business communication research: 5-15% (most articles are paywalled)
    - Open science fields: 30-60% (more open-access content)
"""

import os
import re
import sys
import time
import requests
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Tuple
from urllib.parse import urlparse, quote

# Removed Google Scholar and Archive.is integrations
# These require CAPTCHA solving and are not suitable for automation


# =============================================================================
# CONSTANTS
# =============================================================================

UNPAYWALL_EMAIL = "noreply@andrews.edu"  # Required for Unpaywall API
UNPAYWALL_API = "https://api.unpaywall.org/v2/"
USER_AGENT = "ClassContentGenerator/1.0 (Educational Use)"
REQUEST_TIMEOUT = 30
RATE_LIMIT_DELAY = 1  # Seconds between API calls


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Article:
    """Represents an academic article with metadata and download info."""
    title: str
    authors: str
    year: str
    citation: str
    url: Optional[str]
    doi: Optional[str]
    access_status: str  # "Open access", "Paywalled", "Unknown"
    article_type: str   # "Seminal", "Recent", etc.

    def filename(self) -> str:
        """Generate safe filename for downloaded PDF."""
        # Clean title for filename
        safe_title = re.sub(r'[^\w\s-]', '', self.title)
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        safe_title = safe_title[:50]  # Limit length
        return f"{self.authors.split(',')[0].split()[-1]}-{self.year}-{safe_title}.pdf"


@dataclass
class DownloadResult:
    """Result of attempting to download an article."""
    article: Article
    success: bool
    local_path: Optional[str]
    source: str  # "direct", "unpaywall", "failed"
    message: str


# =============================================================================
# PARSING FUNCTIONS
# =============================================================================

def parse_research_file(research_path: str) -> List[Article]:
    """
    Extract article metadata from research markdown file.

    Expected format:
    ## Article N: Title (TYPE)

    Citation line with DOI

    **URL:** [url]
    **Type:** [type]
    **Access:** [status]
    """
    with open(research_path, 'r', encoding='utf-8') as f:
        content = f.read()

    articles = []

    # Split by article headers
    article_pattern = r'## Article \d+: (.+?)\n\n(.+?)(?=\n## Article|\Z)'
    matches = re.findall(article_pattern, content, re.DOTALL)

    for title_line, article_content in matches:
        # Extract title and type
        title_match = re.match(r'(.+?)\s*\(([^)]+)\)', title_line)
        if title_match:
            title = title_match.group(1).strip()
            article_type = title_match.group(2).strip()
        else:
            title = title_line.strip()
            article_type = "Unknown"

        # Extract citation (first line with author/year)
        citation_match = re.search(r'^([^\n]+\(\d{4}\)[^\n]+)', article_content, re.MULTILINE)
        citation = citation_match.group(1) if citation_match else ""

        # Extract authors and year from citation
        author_match = re.match(r'^([^(]+)\((\d{4})\)', citation)
        if author_match:
            authors = author_match.group(1).strip().rstrip('.,')
            year = author_match.group(2)
        else:
            authors = "Unknown"
            year = "Unknown"

        # Extract DOI
        doi_match = re.search(r'https?://doi\.org/([^\s\)]+)', article_content)
        doi = doi_match.group(1) if doi_match else None

        # Extract URL
        url_match = re.search(r'\*\*URL:\*\*\s*(.+)', article_content)
        url = None
        if url_match:
            url_text = url_match.group(1).strip()
            if url_text.startswith('http'):
                url = url_text

        # Extract access status
        access_match = re.search(r'\*\*Access:\*\*\s*(.+)', article_content)
        access_status = access_match.group(1).strip() if access_match else "Unknown"

        articles.append(Article(
            title=title,
            authors=authors,
            year=year,
            citation=citation,
            url=url,
            doi=doi,
            access_status=access_status,
            article_type=article_type
        ))

    return articles


# =============================================================================
# DOWNLOAD FUNCTIONS
# =============================================================================

def download_pdf(url: str, output_path: str) -> bool:
    """Download PDF from URL to output path."""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, stream=True)

        if response.status_code == 200:
            # Download content
            content = b''
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk

            # Validate it's actually a PDF (check magic bytes)
            if not content.startswith(b'%PDF'):
                print(f"   Not a valid PDF (got {content[:20]}...)")
                return False

            # Write to file
            with open(output_path, 'wb') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"   Error downloading: {e}")
        return False


def try_unpaywall(article: Article) -> Optional[str]:
    """
    Try to find open-access version via Unpaywall API.
    Returns PDF URL if found, None otherwise.
    """
    if not article.doi:
        return None

    try:
        # Clean DOI
        doi = article.doi.strip()

        # Query Unpaywall API
        url = f"{UNPAYWALL_API}{quote(doi)}?email={UNPAYWALL_EMAIL}"
        headers = {'User-Agent': USER_AGENT}

        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            data = response.json()

            # Check if open access version available
            if data.get('is_oa'):
                # Try best_oa_location first
                best_oa = data.get('best_oa_location')
                if best_oa and best_oa.get('url_for_pdf'):
                    return best_oa['url_for_pdf']

                # Fallback to any OA location
                oa_locations = data.get('oa_locations', [])
                for location in oa_locations:
                    if location.get('url_for_pdf'):
                        return location['url_for_pdf']

        return None

    except Exception as e:
        print(f"   Unpaywall error: {e}")
        return None


# Google Scholar and Archive.is functions removed
# These services require CAPTCHA solving and are not suitable for automation


def download_article(article: Article, output_dir: str) -> DownloadResult:
    """
    Attempt to download article using multiple sources.

    Priority:
    1. Direct URL (if open access PDF)
    2. Unpaywall API (if DOI available)
    3. Fallback to reading list
    """
    output_path = os.path.join(output_dir, article.filename())

    # Method 1: Try direct URL
    if article.url and article.url.endswith('.pdf'):
        print(f"   Trying direct URL...")
        if download_pdf(article.url, output_path):
            return DownloadResult(
                article=article,
                success=True,
                local_path=output_path,
                source="direct",
                message="Downloaded from direct URL"
            )

    # Method 2: Try Unpaywall
    if article.doi:
        print(f"   Trying Unpaywall API for DOI: {article.doi}...")
        time.sleep(RATE_LIMIT_DELAY)  # Rate limiting

        unpaywall_url = try_unpaywall(article)
        if unpaywall_url:
            print(f"   Found open-access version via Unpaywall")
            if download_pdf(unpaywall_url, output_path):
                return DownloadResult(
                    article=article,
                    success=True,
                    local_path=output_path,
                    source="unpaywall",
                    message="Downloaded via Unpaywall (legal open-access)"
                )

    # Method 3: Fallback - couldn't download
    return DownloadResult(
        article=article,
        success=False,
        local_path=None,
        source="failed",
        message=f"Paywalled - requires institutional access ({article.access_status})"
    )


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def create_reading_list(articles: List[Article], results: List[DownloadResult],
                       output_dir: str) -> None:
    """Create markdown reading list with download status and access instructions."""

    reading_list_path = os.path.join(output_dir, "READING-LIST.md")

    with open(reading_list_path, 'w', encoding='utf-8') as f:
        f.write("# Weekly Reading Materials\n\n")
        f.write("## Downloaded Articles\n\n")

        # List successful downloads
        downloaded = [r for r in results if r.success]
        if downloaded:
            for result in downloaded:
                f.write(f"### ✅ {result.article.title}\n\n")
                f.write(f"- **File:** `{os.path.basename(result.local_path)}`\n")
                f.write(f"- **Citation:** {result.article.citation}\n")
                f.write(f"- **Source:** {result.source}\n\n")
        else:
            f.write("*No articles successfully downloaded*\n\n")

        f.write("## Articles Requiring Institutional Access\n\n")

        # List failed downloads
        failed = [r for r in results if not r.success]
        if failed:
            for result in failed:
                f.write(f"### ❌ {result.article.title}\n\n")
                f.write(f"- **Citation:** {result.article.citation}\n")
                if result.article.doi:
                    f.write(f"- **DOI:** https://doi.org/{result.article.doi}\n")
                if result.article.url:
                    f.write(f"- **URL:** {result.article.url}\n")
                f.write(f"- **Status:** {result.message}\n\n")

                f.write("**How to access:**\n")
                f.write("1. Check Andrews University or NEU Vietnam library access\n")
                f.write("2. Use university VPN if off-campus\n")
                f.write(f"3. Email author to request PDF: {result.article.authors}\n")
                f.write("4. Check ResearchGate or Academia.edu for author uploads\n\n")
        else:
            f.write("*All articles successfully downloaded!*\n\n")


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main():
    """Command-line entry point."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python tools/download_readings.py [course-code] [week-number]")
        print()
        print("Example:")
        print("  python tools/download_readings.py BCI2AU 1")
        sys.exit(1)

    course_code = sys.argv[1]
    week_number = int(sys.argv[2])

    # Find course folder
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    course_pattern = os.path.join(base_path, "courses", f"{course_code}*")

    import glob
    course_matches = glob.glob(course_pattern)

    if not course_matches:
        print(f"ERROR: Course folder not found for: {course_code}")
        sys.exit(1)

    course_path = course_matches[0]

    # Find research file
    research_file = f"week-{week_number:02d}-research.md"
    research_path = os.path.join(course_path, ".working", "research", research_file)

    if not os.path.exists(research_path):
        print(f"ERROR: Research file not found: {research_path}")
        sys.exit(1)

    # Create output directory
    week_folder = os.path.join(course_path, "weeks", f"week-{week_number:02d}")
    output_dir = os.path.join(week_folder, "output", "readings")
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"DOWNLOADING READING MATERIALS FOR {course_code} WEEK {week_number}")
    print(f"{'='*60}\n")

    # Parse research file
    print(f"Parsing research file: {research_file}")
    articles = parse_research_file(research_path)
    print(f"Found {len(articles)} articles\n")

    # Download articles
    results = []
    for i, article in enumerate(articles, 1):
        print(f"\nArticle {i}/{len(articles)}: {article.title}")
        print(f"   Authors: {article.authors}")
        print(f"   Access: {article.access_status}")

        result = download_article(article, output_dir)
        results.append(result)

        if result.success:
            print(f"   ✅ SUCCESS: {result.message}")
        else:
            print(f"   ❌ FAILED: {result.message}")

    # Create reading list
    print(f"\n{'='*60}")
    print("Creating reading list...")
    create_reading_list(articles, results, output_dir)

    # Summary
    successful = sum(1 for r in results if r.success)
    failed = len(results) - successful

    print(f"\n{'='*60}")
    print("DOWNLOAD SUMMARY")
    print(f"{'='*60}")
    print(f"Total articles: {len(results)}")
    print(f"✅ Downloaded: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"\nOutput directory: {output_dir}")
    print(f"Reading list: {os.path.join(output_dir, 'READING-LIST.md')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
