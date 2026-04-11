#!/usr/bin/env python3
"""
Download baijum81.tripod.com personal website from the Wayback Machine.
"""

import os
import re
import sys
import time
import urllib.request
import urllib.error

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', 'docs', 'tripod')
BASE_DOMAIN = "baijum81.tripod.com"

# (path, timestamp, is_binary)
PAGES = [
    # HTML pages - use earliest available timestamps
    ("/", "20021213122630", False),
    ("/index.html", "20040120181239", False),
    ("/about.html", "20040611012904", False),
    ("/contact.html", "20040130072214", False),
    ("/free-as-in-freedom.html", "20021213170634", False),
    ("/friends.html", "20040120194545", False),
    ("/ooty.html", "20040311154755", False),
    ("/story.html", "20040122063954", False),

    # SMC section
    ("/smc/", "20040414192214", False),
    ("/smc/diff.txt", "20040415011124", False),
    ("/smc/ml", "20191118171828", False),

    # Images
    ("/images/baiju001.jpg", "20070720054414", True),
    ("/images/family1.jpg", "20200509120405", True),
    ("/images/ooty/18.jpg", "20040611214251", True),
    ("/images/ooty/19.jpg", "20040611221130", True),

    # SMC images
    ("/smc/mal-01.png", "20191118171828", True),
    ("/smc/print-01.png", "20141226121106", True),
    ("/smc/print-02.png", "20141226121107", True),
    ("/smc/Screenshot-6.png", "20191118171826", True),

    # SMC font files (SFD are text, TTF is binary)
    ("/smc/free-mal-fonts/AkrutiMal1Bold.sfd", "20040524121417", False),
    ("/smc/free-mal-fonts/AkrutiMal1Normal.sfd", "20040422222821", False),
    ("/smc/free-mal-fonts/AkrutiMal2Bold.sfd", "20040417112454", False),
    ("/smc/free-mal-fonts/AkrutiMal2Normal.sfd", "20040524121000", False),
    ("/smc/free-mal-fonts/MalOtf.ttf", "20040415031301", True),
]


def fetch_wayback(path, timestamp, is_binary=False):
    url = f"http://{BASE_DOMAIN}:80{path}"
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
                # Try without port 80
                url2 = f"http://{BASE_DOMAIN}{path}"
                wayback_url2 = f"https://web.archive.org/web/{timestamp}id_/{url2}"
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
    if not isinstance(content, str):
        return content

    # Remove Wayback Machine injected content
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

    # Fix URLs: remove Wayback Machine URL prefixes
    content = re.sub(
        r'https?://web\.archive\.org/web/\d+(?:id_|im_|js_|cs_)?/https?://baijum81\.tripod\.com(?::80)?',
        '', content)

    # Remove Tripod ad scripts/iframes (they won't work anyway)
    content = re.sub(
        r'<script[^>]*src="[^"]*tripod\.com/adm/[^"]*"[^>]*>.*?</script>',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<iframe[^>]*tripod[^>]*>.*?</iframe>',
        '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(
        r'<noscript>.*?tripod.*?</noscript>',
        '', content, flags=re.DOTALL | re.IGNORECASE)

    # Remove Wayback Machine comment blocks
    content = re.sub(
        r'<!--\s*FILE ARCHIVED ON.*?-->',
        '', content, flags=re.DOTALL)
    content = re.sub(
        r'<!--\s*playback timings.*?-->',
        '', content, flags=re.DOTALL)

    return content


def save_file(path, content, is_binary=False):
    if path == '/':
        filepath = os.path.join(OUTPUT_DIR, 'index-root.html')
    elif path.endswith('/'):
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
    print("Downloading baijum81.tripod.com from Wayback Machine")
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
