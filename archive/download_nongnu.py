#!/usr/bin/env python3
"""
Download www.nongnu.org/smc/ website from the Wayback Machine.
"""

import os
import re
import sys
import time
import urllib.request
import urllib.error

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', 'docs', 'nongnu-smc')

# (path, timestamp, is_binary)
# Use earliest timestamps for original content by Baiju
PAGES = [
    # Root docs
    ("/smc/docs/", "20081007000528", False),
    ("/smc/docs/index.html", "20030625230605", False),
    ("/smc/docs/old-index.html", "20211018224025", False),
    ("/smc/docs/faq.html", "20030727174848", False),
    ("/smc/docs/howto.txt", "20030519081613", False),
    ("/smc/docs/input-methods.html", "20030727175329", False),
    ("/smc/webmasters.html", "20030625034643", False),

    # Presentations
    ("/smc/docs/chillu-presentation/", "20211018230838", False),
    ("/smc/docs/chillu-presentation/chillu.html", "20130811105854", False),
    ("/smc/docs/smc-presentation/", "20211018232608", False),
    ("/smc/docs/smc-presentation/smc.html", "20130205064442", False),
    ("/smc/docs/smc-presentation2/", "20211018224203", False),
    ("/smc/docs/unicode-presentation/", "20211019001332", False),
    ("/smc/docs/unicode-presentation/unicode.html", "20120316215911", False),
    ("/smc/docs/kde-presentation/", "20211018224834", False),

    # Other docs
    ("/smc/docs/rendering-basics/", "20211018224423", False),
    ("/smc/docs/debian/", "20211019002836", False),
    ("/smc/docs/printer/", "20211019002211", False),
    ("/smc/docs/printer/fedora/", "20211204103519", False),
    ("/smc/docs/synaptic/", "20211018233243", False),
    ("/smc/docs/synaptic/0-synaptic.html", "20211205223001", False),
    ("/smc/docs/synaptic/1-menu.html", "20211206003215", False),

    # Images
    ("/smc/docs/images/0d0c.png", "20050218080513", True),
    ("/smc/docs/images/0d60.png", "20050218083023", True),
    ("/smc/docs/images/0d61.png", "20191202081130", True),
    ("/smc/docs/images/ml_inscript_layout.jpg", "20061213043830", True),
    ("/smc/docs/images/sdp-title.jpg", "20060512141840", True),
    ("/smc/images/smc-final.jpg", "20051018200853", True),
]


def fetch_wayback(path, timestamp, is_binary=False):
    for prefix in ["http://www.nongnu.org:80", "https://www.nongnu.org", "http://www.nongnu.org"]:
        url = f"{prefix}{path}"
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
                        try:
                            return data.decode('utf-8')
                        except UnicodeDecodeError:
                            return data.decode('latin-1')
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    break  # Try next prefix
                elif e.code == 429:
                    time.sleep(10 * (attempt + 1))
                else:
                    break
            except Exception:
                if attempt < 2:
                    time.sleep(2)
                else:
                    break
    return None


def clean_html(content):
    if not isinstance(content, str):
        return content
    content = re.sub(
        r'<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<script[^>]*src="[^"]*web-static\.archive\.org[^"]*"[^>]*>.*?</script>',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<script[^>]*>.*?__wm\..*?</script>',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<script>window\.RufflePlayer.*?</script>',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<link[^>]*href="[^"]*web-static\.archive\.org[^"]*"[^>]*/>',
        '', content)
    content = re.sub(
        r'https?://web\.archive\.org/web/\d+(?:id_|im_|js_|cs_)?/https?://www\.nongnu\.org(?::80)?',
        '', content)
    content = re.sub(
        r'<!--\s*FILE ARCHIVED ON.*?-->',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<!--\s*playback timings.*?-->',
        '', content, flags=re.DOTALL)
    return content


def save_file(path, content, is_binary=False):
    if path.endswith('/'):
        filepath = os.path.join(OUTPUT_DIR, path.lstrip('/'), 'index.html')
    else:
        filepath = os.path.join(OUTPUT_DIR, path.lstrip('/'))

    # Strip the /smc/ prefix for cleaner directory structure
    filepath = filepath.replace('/smc/', '/', 1)

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
    print("Downloading www.nongnu.org/smc/ from Wayback Machine")
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
        time.sleep(0.5)

    print(f"\n{'=' * 60}")
    print(f"Done: {success} downloaded, {failed} failed")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
