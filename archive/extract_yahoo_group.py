#!/usr/bin/env python3
"""
Extract malayalamlinux Yahoo Group messages from the Wayback Machine.

This script:
1. Uses the Wayback CDX API to find all captured pages
2. Downloads message listing pages and individual message pages
3. Extracts message metadata and content
4. Saves everything in readable text and mbox format
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from html import unescape
from html.parser import HTMLParser

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
GROUP_NAME = "malayalamlinux"
BASE_URL = "groups.yahoo.com/group/malayalamlinux"

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip = True
        if tag == 'br':
            self.result.append('\n')
        if tag == 'p':
            self.result.append('\n\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            self.result.append(data)

    def get_text(self):
        return ''.join(self.result).strip()


def html_to_text(html_str):
    extractor = HTMLTextExtractor()
    try:
        extractor.feed(unescape(html_str))
        return extractor.get_text()
    except:
        return re.sub(r'<[^>]+>', '', unescape(html_str)).strip()


def fetch_url(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; archive-research)'
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode('latin-1')
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif e.code == 404:
                return None
            else:
                print(f"  HTTP {e.code} for {url}")
                return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                print(f"  Error: {e}")
                return None
    return None


def get_cdx_entries():
    """Get all Wayback Machine captures for the group."""
    url = (f"https://web.archive.org/cdx/search/cdx?"
           f"url={BASE_URL}*&output=json&fl=timestamp,original,statuscode,mimetype")
    content = fetch_url(url)
    if not content:
        return []

    data = json.loads(content)
    if len(data) < 2:
        return []

    headers = data[0]
    entries = []
    for row in data[1:]:
        entry = dict(zip(headers, row))
        entries.append(entry)
    return entries


def extract_messages_from_listing(html_content):
    """Extract message info from a Yahoo Groups message listing page."""
    messages = []

    # Pattern for message links with subjects
    pattern = r'message/(\d+)[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html_content)

    for msg_num, subject in matches:
        subject = unescape(subject.strip())
        messages.append({
            'number': int(msg_num),
            'subject': subject,
        })

    return messages


def extract_message_content(html_content):
    """Extract message content from an individual message page."""
    result = {}

    # Check if this is a 999 error page
    if 'This page is currently unavailable' in html_content:
        return None

    # Try to extract subject
    subj_patterns = [
        r'<span[^>]*class="[^"]*subject[^"]*"[^>]*>([^<]+)</span>',
        r'<td[^>]*class="[^"]*subject[^"]*"[^>]*>([^<]+)</td>',
        r'Subject:\s*([^<\n]+)',
    ]
    for pattern in subj_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            result['subject'] = unescape(match.group(1).strip())
            break

    # Try to extract author/from
    from_patterns = [
        r'<span[^>]*class="[^"]*from[^"]*"[^>]*>([^<]+)</span>',
        r'From:\s*([^<\n]+)',
        r'<a[^>]*class="[^"]*author[^"]*"[^>]*>([^<]+)</a>',
    ]
    for pattern in from_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            result['from'] = unescape(match.group(1).strip())
            break

    # Try to extract date
    date_patterns = [
        r'<span[^>]*class="[^"]*date[^"]*"[^>]*>([^<]+)</span>',
        r'Date:\s*([^<\n]+)',
    ]
    for pattern in date_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            result['date'] = unescape(match.group(1).strip())
            break

    # Try to extract message body
    body_patterns = [
        r'<div[^>]*id="[^"]*ygrps-yiv[^"]*"[^>]*>(.*?)</div>\s*(?:</div>|<div)',
        r'<div[^>]*class="[^"]*msg-content[^"]*"[^>]*>(.*?)</div>',
        r'<td[^>]*class="[^"]*msgBody[^"]*"[^>]*>(.*?)</td>',
        r'<!-- start content -->(.*?)<!-- end content -->',
    ]
    for pattern in body_patterns:
        match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
        if match:
            result['body'] = html_to_text(match.group(1))
            break

    return result if result else None


def save_messages_text(messages, filepath):
    """Save messages as a readable text file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 78 + "\n")
        f.write("Malayalam GNU/Linux Project Group - Yahoo Groups Archive\n")
        f.write(f"Group: malayalamlinux@yahoogroups.com\n")
        f.write(f"Created: December 21, 2001\n")
        f.write(f"Members: 55\n")
        f.write(f"Category: /Computers & Internet/Software/Operating Systems/Unix/Linux/\n")
        f.write(f"Description: Malayalam GNU/Linux Project Group\n")
        f.write(f"Later became: Swathanthra Malayalam Computing (SMC)\n")
        f.write(f"  https://savannah.nongnu.org/projects/smc\n")
        f.write(f"  https://smc.org.in\n")
        f.write(f"\nExtracted from Wayback Machine on {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("=" * 78 + "\n\n")

        for msg in sorted(messages, key=lambda m: m.get('number', 0)):
            f.write("-" * 78 + "\n")
            f.write(f"Message #{msg.get('number', '?')}")
            if msg.get('subject'):
                f.write(f": {msg['subject']}")
            f.write("\n")
            if msg.get('from'):
                f.write(f"From: {msg['from']}\n")
            if msg.get('date'):
                f.write(f"Date: {msg['date']}\n")
            if msg.get('body'):
                f.write(f"\n{msg['body']}\n")
            else:
                f.write("(message body not available in archive)\n")
            f.write("\n")

    print(f"Saved {len(messages)} messages to {filepath}")


def save_messages_json(messages, filepath):
    """Save messages as JSON for further processing."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump({
            'group': 'malayalamlinux',
            'title': 'Malayalam GNU/Linux Project Group',
            'created': '2001-12-21',
            'members': 55,
            'extracted': datetime.now().isoformat(),
            'source': 'Wayback Machine (web.archive.org)',
            'messages': sorted(messages, key=lambda m: m.get('number', 0))
        }, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(messages)} messages to {filepath}")


def main():
    print("=" * 60)
    print("Malayalam GNU/Linux Yahoo Group Archive Extractor")
    print("=" * 60)

    all_messages = {}

    # Step 1: Get CDX entries
    print("\n[1/4] Fetching Wayback Machine index...")
    entries = get_cdx_entries()
    print(f"  Found {len(entries)} captures")

    # Step 2: Process message listing pages (status 200)
    print("\n[2/4] Downloading message listing pages...")
    listing_urls = [
        ("20031216130914", "http://groups.yahoo.com:80/group/malayalamlinux/messages/235"),
        ("20041212192709", "http://groups.yahoo.com:80/group/malayalamlinux/messages/61"),
        ("20031216205858", "http://groups.yahoo.com:80/group/malayalamlinux/messages/82"),
    ]

    for timestamp, url in listing_urls:
        wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
        print(f"  Fetching {url}...")
        content = fetch_url(wayback_url)
        if content:
            msgs = extract_messages_from_listing(content)
            for msg in msgs:
                num = msg['number']
                if num not in all_messages:
                    all_messages[num] = msg
                else:
                    # Merge: keep more complete data
                    for k, v in msg.items():
                        if v and not all_messages[num].get(k):
                            all_messages[num][k] = v
            print(f"    Found {len(msgs)} messages")
        time.sleep(1)

    # Step 3: Try individual message pages
    print("\n[3/4] Attempting to fetch individual message pages...")

    # Get all message entries from CDX
    message_entries = [e for e in entries if '/message/' in e['original'] and e['statuscode'] != '-']

    # Also try message numbers we know about but might not be in CDX
    known_numbers = set(all_messages.keys())
    max_msg = max(known_numbers) if known_numbers else 236

    fetched_count = 0
    skipped_count = 0

    for entry in message_entries:
        match = re.search(r'/message/(\d+)', entry['original'])
        if not match:
            continue
        msg_num = int(match.group(1))

        # Try fetching even 999 pages - sometimes Wayback stores content
        wayback_url = f"https://web.archive.org/web/{entry['timestamp']}/{entry['original']}"
        content = fetch_url(wayback_url)

        if content:
            msg_data = extract_message_content(content)
            if msg_data:
                msg_data['number'] = msg_num
                if msg_num not in all_messages:
                    all_messages[msg_num] = msg_data
                else:
                    for k, v in msg_data.items():
                        if v and not all_messages[msg_num].get(k):
                            all_messages[msg_num][k] = v
                fetched_count += 1
                print(f"  Message #{msg_num}: extracted content")
            else:
                skipped_count += 1
                print(f"  Message #{msg_num}: no content (error page)")

        time.sleep(0.5)  # Be nice to the Wayback Machine

    print(f"  Fetched: {fetched_count}, Skipped: {skipped_count}")

    # Step 4: Try the group info page from neo interface
    print("\n[4/4] Fetching group metadata...")
    neo_urls = [
        ("20141229172341", "https://groups.yahoo.com/neo/groups/malayalamlinux/info"),
        ("20191217153419", "https://groups.yahoo.com/api/v1/groups/malayalamlinux/"),
    ]

    for timestamp, url in neo_urls:
        wayback_url = f"https://web.archive.org/web/{timestamp}/{url}"
        print(f"  Fetching {url}...")
        content = fetch_url(wayback_url)
        if content and 'api/v1' in url:
            try:
                data = json.loads(content)
                group_data = data.get('ygData', {})
                print(f"    Group: {group_data.get('title', 'N/A')}")
                print(f"    Created: {datetime.fromtimestamp(group_data.get('dateCreated', 0)).strftime('%Y-%m-%d')}")
                print(f"    Messages visible: {group_data.get('messagesVis', 'N/A')}")
            except:
                pass
        time.sleep(1)

    # Save results
    print(f"\n{'=' * 60}")
    print(f"Total messages found: {len(all_messages)}")
    print(f"Message numbers: {sorted(all_messages.keys())}")

    if all_messages:
        messages_list = list(all_messages.values())

        text_path = os.path.join(OUTPUT_DIR, "malayalamlinux_messages.txt")
        save_messages_text(messages_list, text_path)

        json_path = os.path.join(OUTPUT_DIR, "malayalamlinux_messages.json")
        save_messages_json(messages_list, json_path)

    # Print summary
    print(f"\n{'=' * 60}")
    print("IMPORTANT NOTE:")
    print("The Wayback Machine only captured a fraction of the messages.")
    print(f"Messages found: {len(all_messages)} (up to #{max_msg})")
    print()
    print("The full archive exists as a private WARC file on archive.org:")
    print("  Item: yahoo-groups-2017-04-01T21-03-27Z-cdf32a")
    print("  File: malayalamlinux.t2r3gpB.warc.gz (617 KB)")
    print("  Status: PRIVATE (requires special access)")
    print()
    print("To request access to the full archive, you can:")
    print("1. Email Archive Team: archiveteam@archiveteam.org")
    print("2. Contact the Internet Archive: info@archive.org")
    print("3. Check: https://datahorde.org/how-to-recover-your-yahoo-groups-from-the-internet-archive/")
    print("=" * 60)


if __name__ == '__main__':
    main()
