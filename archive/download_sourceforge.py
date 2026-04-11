#!/usr/bin/env python3
"""
Download the archived malayalamlinux.sourceforge.net site from the Wayback Machine.
Reconstructs the directory structure and downloads all HTML, text, and image files.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import urlparse, unquote

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', 'docs', 'sourceforge')
BASE_DOMAIN = "malayalamlinux.sourceforge.net"

# Pages to download: (path, preferred_timestamp, is_binary)
# We pick the earliest good capture for each page to get the most original content
PAGES = [
    # Root
    ("/", "20020923021004", False),
    ("/index-ml.html", "20030608103527", False),
    ("/README", "20030608103527", False),
    ("/pango-diff.txt", "20030608103527", False),

    # Documents
    ("/documents/", "20030608103527", False),
    ("/documents/project.html", "20030608103527", False),
    ("/documents/faq.html", "20030608103527", False),
    ("/documents/links.html", "20030608103527", False),

    # Bookmarks
    ("/bookmarks/", "20030608103527", False),
    ("/bookmarks/bookmarks.html", "20030608103527", False),
    ("/bookmarks/l10n-projects.html", "20030608103527", False),

    # Downloads directory listing
    ("/downloads/", "20030608103527", False),
    ("/downloads/downloads.html", "20030608103527", False),
    ("/downloads/COPYING", "20030608103527", False),

    # Input methods
    ("/input-methods/", "20030608103527", False),
    ("/input-methods/Compose", "20030608103527", False),
    ("/input-methods/ml", "20030608103527", False),
    ("/input-methods/ml_IN", "20030608103527", False),
    ("/input-methods/ml_setkb", "20030608103527", False),

    # OpenOffice
    ("/open-office/", "20030608103527", False),
    ("/open-office/ml-oo.html", "20030608103527", False),
    ("/open-office/Compose", "20030608103527", False),
    ("/open-office/ml_IN", "20030608103527", False),
    ("/open-office/fonts.dir", "20030608103527", False),
    ("/open-office/compose.dir", "20030608103527", False),

    # HOWTO
    ("/HOWTO/", "20030608103527", False),
    ("/HOWTO/HOWTO.txt", "20030608103527", False),
    ("/HOWTO/README", "20030608103527", False),

    # Translations
    ("/translations/", "20030608103527", False),
    ("/translations/sorted.txt", "20030608103527", False),
    ("/translations/words-new.txt", "20030608103527", False),
    ("/translations/ml-po-files/", "20030608103527", False),
    ("/translations/ml-po-files/glossary.po", "20030608103527", False),

    # Education
    ("/edu/", "20030608103527", False),
    ("/edu/index.html", "20030608103527", False),
    ("/edu/glue/index.html", "20030608103527", False),
    ("/edu/glue/left.html", "20030608103527", False),
    ("/edu/glue/FS/index.html", "20030608103527", False),
    ("/edu/proposal-by-ajith.html", "20030608103527", False),

    # Web development
    ("/web-devel/", "20030608103527", False),
    ("/web-devel/index-en.html", "20030608103527", False),
    ("/web-devel/index-ml.html", "20030608103527", False),

    # Font development
    ("/font-devel/", "20030608103527", False),

    # Fonts directory
    ("/downloads/fonts/", "20030608103527", False),

    # Screen shots
    ("/screen-shots/", "20030608103527", False),

    # Test
    ("/test/", "20030608103527", False),

    # Images - binary
    ("/screen-shots/gnome-mal.png", "20030608103527", True),
    ("/screen-shots/malayalam.png", "20030608103527", True),
    ("/screen-shots/ml_dates.png", "20030608103527", True),
    ("/screen-shots/snapshot1.png", "20030608103527", True),
    ("/screen-shots/yudit01.png", "20030608103527", True),
    ("/screen-shots/after-sorting.png", "20030608103527", True),
    ("/screen-shots/before-sorting.png", "20030608103527", True),
    ("/screen-shots/root.jpg", "20030608103527", True),
    ("/input-methods/0d0c.png", "20030608103527", True),
    ("/input-methods/0d60.png", "20030608103527", True),
    ("/input-methods/0d61.png", "20030608103527", True),
    ("/input-methods/ml_inscript_layout.jpg", "20030608103527", True),
    ("/downloads/ml_inscript_layout.jpg", "20030608103527", True),
    ("/edu/gnu-head-sm.jpg", "20030608103527", True),

    # Source files
    ("/input-methods/immalayalam-translit.c", "20030608103527", False),
    ("/input-methods/inscript.ml.xmm", "20030608103527", False),
    ("/downloads/nonstdml-map.xmm", "20030608103527", False),
    ("/downloads/ml", "20030608103527", False),
    ("/downloads/ml_IN", "20030608103527", False),
    ("/downloads/ml_setkb", "20030608103527", False),
    ("/open-office/nonstdml-map.xmm", "20030608103527", False),
]


def fetch_wayback(path, timestamp, is_binary=False):
    """Fetch a page from the Wayback Machine using the raw (id_) prefix."""
    url = f"http://{BASE_DOMAIN}:80{path}"
    # Use id_ prefix to get the original content without Wayback toolbar
    wayback_url = f"https://web.archive.org/web/{timestamp}id_/{url}"

    for attempt in range(3):
        try:
            req = urllib.request.Request(wayback_url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; archive-research)'
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                if is_binary:
                    return resp.read()
                else:
                    data = resp.read()
                    # Try UTF-8 first, fall back to latin-1
                    try:
                        return data.decode('utf-8')
                    except UnicodeDecodeError:
                        return data.decode('latin-1')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Try without id_ prefix
                wayback_url2 = f"https://web.archive.org/web/{timestamp}/{url}"
                try:
                    req2 = urllib.request.Request(wayback_url2, headers={
                        'User-Agent': 'Mozilla/5.0 (compatible; archive-research)'
                    })
                    with urllib.request.urlopen(req2, timeout=30) as resp2:
                        if is_binary:
                            return resp2.read()
                        else:
                            data = resp2.read()
                            try:
                                return data.decode('utf-8')
                            except UnicodeDecodeError:
                                return data.decode('latin-1')
                except:
                    pass
                return None
            elif e.code == 429:
                wait = 10 * (attempt + 1)
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"    HTTP {e.code}")
                return None
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                print(f"    Error: {e}")
                return None
    return None


def clean_html(content):
    """Remove Wayback Machine injected content from HTML."""
    if not isinstance(content, str):
        return content

    # Remove Wayback Machine toolbar/banner
    content = re.sub(
        r'<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->',
        '', content, flags=re.DOTALL)

    # Remove Wayback Machine scripts
    content = re.sub(
        r'<script[^>]*src="[^"]*web-static\.archive\.org[^"]*"[^>]*>.*?</script>',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<script[^>]*>.*?__wm\..*?</script>',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<script>window\.RufflePlayer.*?</script>',
        '', content, flags=re.DOTALL)

    # Remove Wayback Machine CSS
    content = re.sub(
        r'<link[^>]*href="[^"]*web-static\.archive\.org[^"]*"[^>]*/>',
        '', content)

    # Fix URLs: remove Wayback Machine URL prefixes
    content = re.sub(
        r'https?://web\.archive\.org/web/\d+(?:id_|im_|js_|cs_)?/https?://malayalamlinux\.sourceforge\.net(?::80)?',
        '', content)
    content = re.sub(
        r'https?://web\.archive\.org/web/\d+(?:id_|im_|js_|cs_)?/http://malayalamlinux\.sourceforge\.net(?::80)?',
        '', content)

    # Remove Wayback Machine comment blocks
    content = re.sub(
        r'<!--\s*FILE ARCHIVED ON.*?-->',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<!--\s*playback timings.*?-->',
        '', content, flags=re.DOTALL)

    return content


def save_file(path, content, is_binary=False):
    """Save content to the output directory."""
    # Convert URL path to filesystem path
    if path.endswith('/'):
        filepath = os.path.join(OUTPUT_DIR, path.lstrip('/'), 'index.html')
    else:
        filepath = os.path.join(OUTPUT_DIR, path.lstrip('/'))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if is_binary:
        with open(filepath, 'wb') as f:
            f.write(content)
    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return filepath


def main():
    print("=" * 60)
    print("Downloading malayalamlinux.sourceforge.net from Wayback Machine")
    print("=" * 60)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    success = 0
    failed = 0

    for path, timestamp, is_binary in PAGES:
        print(f"  {path}...", end=" ", flush=True)
        content = fetch_wayback(path, timestamp, is_binary)

        if content is None:
            print("FAILED")
            failed += 1
            continue

        if not is_binary:
            content = clean_html(content)

        filepath = save_file(path, content, is_binary)
        size = len(content) if isinstance(content, str) else len(content)
        print(f"OK ({size:,} bytes)")
        success += 1

        time.sleep(0.5)  # Be nice to Wayback Machine

    print(f"\n{'=' * 60}")
    print(f"Done: {success} downloaded, {failed} failed")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
