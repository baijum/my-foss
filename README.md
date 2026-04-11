# Malayalam GNU/Linux Project Group - Yahoo Groups Archive

This repository contains a partial archive recovery of the **malayalamlinux** Yahoo
Group, the original mailing list for the Malayalam GNU/Linux Project.

## Group History

- **Group name:** malayalamlinux
- **Email:** malayalamlinux@yahoogroups.com
- **Created:** December 21, 2001
- **Founded by:** Baiju M, student at NIT Calicut
- **Members:** 55
- **Category:** Computers & Internet / Software / Operating Systems / Unix / Linux
- **Active period:** 2001-2003
- **SourceForge project:** https://sourceforge.net/projects/malayalamlinux/ (registered 2002-01-17)
- **Subscription address:** malayalamlinux-subscribe@yahoogroups.com

In 2001, this community started as "Malayalam Linux Online" with the goal of
translating X, GNOME, and KDE into Malayalam. About ten months later, it adopted
the name **Swathanthra Malayalam Computing (SMC)** and moved to Savannah:
https://savannah.nongnu.org/projects/smc

SMC went on to become India's largest language technology developer community,
maintaining Malayalam fonts and tools upstream for Fedora, Debian, GNOME, KDE,
Firefox, and LibreOffice. It is now at https://smc.org.in

## What's in This Archive

### Recovered Data

| File | Description |
|------|-------------|
| `archive/malayalamlinux_messages.txt` | 53 message subjects in readable text format |
| `archive/malayalamlinux_messages.json` | Same data in JSON format |
| `archive/extract_yahoo_group.py` | Python script used to extract data from the Wayback Machine |

### Recovered Message Subjects (53 of 236+)

Messages #61-111 and #235-236 were recovered from Wayback Machine listing pages.
Topics discussed include:

- Malayalam in GTK2 (messages #62-65)
- Technical terms translation (#76)
- KBip project (#80-81)
- Varamozhi (#84, #106)
- Unicode Malayalam (#86-96)
- The linguistic properties of Malayalam "Chillaksharam"s (#92, #97-98)
- Sorting cillus (#99)
- Indic computing standards (#102-104, #107, #110-111)
- How to encode chillu glyphs in Unicode (#108)
- Bill Gates Promis to Mallus (#235)
- Showcasing Indian language support in OpenSource stall at Linux (#236)

### Recovered SourceForge Website (67 files)

The project website at `malayalamlinux.sourceforge.net` has been fully recovered
from the Wayback Machine. 67 files were downloaded including:

- Project details, FAQ, and Malayalam International HOWTO
- Malayalam fonts (TTF/OTF) metadata and GPL license
- GTK+ transliteration input method source code (C)
- Inscript keyboard layout and Compose files
- OpenOffice.org Malayalam support guide
- Translation glossary (English-Malayalam, 131 KB PO file)
- Screenshots of Malayalam rendering in GNOME, Yudit, and locale
- Education proposals (Computer Laboratory for Schools)
- Curated bookmarks and L10n project links

Files are in `docs/sourceforge/` and viewable at `docs/sourceforge-site.html`.

### Recovered Personal Website (24 files)

The personal website at `baijum81.tripod.com` has been fully recovered from the
Wayback Machine. 24 files downloaded including:

- Personal pages: About, Story (biography), Friends, Contact, "Free as in Freedom"
- Photos: Profile photo, 1984 family photo from Mukkam, Ooty trip photos
- SMC section: 4 Malayalam rendering screenshots, Pango diff, XKB layout
- Font sources: 4 Akruti Malayalam FontForge (.sfd) files + MalOtf.ttf

Files are in `docs/tripod/` and viewable at `docs/tripod-site.html`.

### Recovered Savannah News Posts (9 posts)

8 deleted news posts by baijum81 on the SMC Savannah project page were recovered
from a [May 2012 Wayback Machine snapshot](https://web.archive.org/web/20120529231604/http://savannah.nongnu.org/news/?group=smc).
Only titles, dates, and authorship were captured -- the individual news pages
were never archived by the Wayback Machine.

| ID | Date | Title |
|----|------|-------|
| 1148 | 2002-10-21 | Swathanthra Malayalam Computing Project |
| 1151 | 2002-10-22 | SMC Mailing Lists |
| 1164 | 2002-10-25 | Website updated |
| 1187 | 2002-10-31 | GPL translation |
| 1234 | 2002-11-15 | Malayalam in GNOME 2 |
| 1282 | 2002-11-29 | Akruti Malayalam fonts |
| 1603 | 2003-03-01 | GNU Emacs now supports Malayalam |
| 1616 | 2003-03-03 | Free 8-bit Malayalam fonts |
| 4572 | 2006-09-18 | SMC Reloaded! (handover post, still live) |

### What's Missing

- **Message bodies** -- Yahoo returned 999 (bot blocking) for individual message
  pages, so the Wayback Machine only saved error pages, not actual content.
- **Messages #1-60 and #112-234** -- These ranges were not captured in any
  Wayback Machine listing page snapshots.
- **Files, photos, and member list** -- Not captured by the Wayback Machine.

## The Full Archive (Restricted)

The complete message archive exists as a WARC file on the Internet Archive, but is
currently access-restricted:

- **Item:** `yahoo-groups-2017-04-01T21-03-27Z-cdf32a`
- **File:** `malayalamlinux.t2r3gpB.warc.gz` (617 KB)
- **Collection:** Archive Team Yahoo! Groups (`archiveteam_yahoogroups`)
- **Status:** `access-restricted-item: true`, all files marked `private: true`
- **Uploader:** `lars+archive@6xq.net` (Archive Team)
- **Item URL:** https://archive.org/details/yahoo-groups-2017-04-01T21-03-27Z-cdf32a

This WARC file was captured via the Yahoo Groups API in April 2017 and contains
JSON-formatted message data. Once obtained, the `extract_yahoo_group.py` script
can be extended to parse the WARC and extract full message bodies.

## Wayback Machine Captures

The following Wayback Machine snapshots were used for this recovery:

| Date | URL | Status | Content |
|------|-----|--------|---------|
| 2004-11-27 | `/group/malayalamlinux/` | 200 | Group homepage |
| 2004-12-12 | `/group/malayalamlinux/messages/61` | 200 | Message listing (msgs #61-90) |
| 2003-12-16 | `/group/malayalamlinux/messages/82` | 200 | Message listing (msgs #82-111) |
| 2003-12-16 | `/group/malayalamlinux/messages/235` | 200 | Message listing (msgs #235-236) |
| 2014-12-24 | `/neo/groups/malayalamlinux/info` | 200 | Neo-interface group info |
| 2019-12-17 | `/api/v1/groups/malayalamlinux/` | 200 | API group metadata (JSON) |

## TODO

- [ ] **Request access to the full WARC archive.** Email the following as the
      original group founder to request access:
  - Archive Team uploader: `lars+archive@6xq.net`
  - Archive Team: `archiveteam@archiveteam.org`
  - Internet Archive: `info@archive.org`
  - Reference item: `yahoo-groups-2017-04-01T21-03-27Z-cdf32a`
  - Reference guide: https://datahorde.org/how-to-recover-your-yahoo-groups-from-the-internet-archive/
- [ ] **Parse WARC file once obtained.** Extend `extract_yahoo_group.py` to parse
      the WARC file (contains Yahoo Groups API JSON responses) and extract full
      message bodies, authors, and dates into readable format (text and mbox).
- [ ] **Check with other early members** (karunakar, shaji, and others listed on
      the SourceForge project) whether anyone has personal email archives of
      the mailing list from 2001-2003.
- [ ] **Check personal email archives.** Messages sent to the group were also
      delivered to members via email. Old email backups may contain the full
      message history.
- [ ] **Cross-reference with SMC archives.** Some discussions may have continued
      on the SMC mailing lists at `lists.smc.org.in` after the group was renamed.

## Yahoo Groups Shutdown Timeline

- **2019-10-28** -- Uploading new content disabled
- **2019-12-14** -- All content made unavailable
- **2020-10-12** -- Creation of new groups disabled
- **2020-12-16** -- Web interface and mailing lists shut down permanently

## Related Links

- Swathanthra Malayalam Computing: https://smc.org.in
- SMC on Savannah: https://savannah.nongnu.org/projects/smc
- SMC on Wikipedia: https://en.wikipedia.org/wiki/Swathanthra_Malayalam_Computing
- SourceForge project: https://sourceforge.net/projects/malayalamlinux/
- 12th year of SMC: https://12.smc.org.in/en.html
- Archive Team Yahoo! Groups: https://archive.org/details/archiveteam_yahoogroups
- Yahoo Groups recovery guide: https://datahorde.org/how-to-recover-your-yahoo-groups-from-the-internet-archive/
