# Latest stable Python 3 release

- **Date:** 2026-09-28
- **Card:** Brief: Latest stable Python release (`marketing/briefs/2026-09-28-research-test-a.md`)
- **Role:** researcher
- **Sources checked:** 2026-09-28 (UTC)

## Question

What is the latest stable Python 3 release today (2026-09-28), and on what date was it released?
Use python.org as the source.

## Short answer

- The latest stable Python 3 release as of 2026-09-28 is **Python 3.14.7**.
- It was released on **August 5, 2026** (python.org writes the date as "Aug. 5, 2026").
- 3.14.7 is the seventh maintenance (bugfix) release of the 3.14 series.
- Python 3.15 is still a pre-release series (3.15.0rc1, release candidate); it is not yet stable.
  python.org's active-releases table lists 3.15 as "pre-release" with a planned first release of
  2026-10-01. So 3.15 does not displace 3.14.7 as the latest stable release.
- Latest stable release in each maintained series, for context: 3.14.7 (Aug. 5, 2026),
  3.13.14 (June 10, 2026), 3.12.13 (March 3, 2026).

## Findings

Primary source: python.org release page for 3.14.7 —
https://www.python.org/downloads/release/python-3147/ (checked 2026-09-28).

- The page states, verbatim: "**Release date:** Aug. 5, 2026" and "This is the seventh
  maintenance release of Python 3.14 ... containing around 499 bugfixes, build improvements and
  documentation changes from 86 contributors since 3.14.6."
- python.org's download index (https://www.python.org/downloads/, checked 2026-09-28) offers
  "Download Python 3.14.7" as the current latest version, with the version table row
  "Python 3.14.7  Aug. 5, 2026".
- The active-releases table on that page lists 3.15 as "pre-release" (first released / planned
  2026-10-01, per PEP 790), and 3.14 as "bugfix" (first released 2025-10-07, per PEP 745).
  A series listed as "pre-release" is not the stable release.
- Each of 3.14.5's and 3.14.6's own release pages carries a banner "has been superseded by
  Python 3.14.7", corroborating that 3.14.7 is the newest stable 3.14 point release
  (https://www.python.org/downloads/release/python-3146/, checked 2026-09-28).

### Source-quality note (worth recording)

The first automated extraction of https://www.python.org/downloads/ returned a **stale cached
copy** that still showed 3.14.6 (June 10, 2026) as the newest release and did not list the
3.14.7 row. The authoritative release page (python.org/downloads/release/python-3147/) and a
fresh fetch of the download index both show 3.14.7 (Aug. 5, 2026). Lesson: for "what is latest"
questions, trust the specific release page URL (and cross-check a second python.org URL), not a
single cached fetch of a listing page.

## What this means for us

Not a competitive/market question — this card is a test of the Research column. The only
product-relevant read: if any of our tooling pins a Python version or advertises "latest Python",
the current stable target is 3.14.7. There is no action implied for customers, competitors or
markets. **No claim here affects marketing positioning.**

## Confidence and gaps

- **Confidence: high.** The answer comes directly from python.org's own release page and download
  index, both fetched on the day in question, and is consistent across two python.org URLs plus the
  supersede-banners on the 3.14.5/3.14.6 pages.
- **Gap:** python.org's download index short-circuits to the "latest" release, so it does not by
  itself enumerate a full release feed; that is fine here because the release page is explicit.
- **Caveat:** "stable" is interpreted as a final (non-pre-release, non-alpha/beta/rc) release.
  If the operator means "latest release of any kind", then 3.15.0rc1 (a release candidate) would be
  newer — but that is not stable. Flagging the ambiguity; the brief says "stable", so 3.14.7 is the
  answer.

## Suggested next steps

- None required. This is a self-contained factual answer for a Research-column test card.
- If a follow-up is wanted: a recurring `competitor-news-monitor`-style watch on python.org's
  release feed could auto-flag new stable releases (3.15.0 stable is currently planned for
  2026-10-01 per PEP 790), but that is optional and outside this brief.
