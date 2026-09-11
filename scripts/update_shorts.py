#!/usr/bin/env python3
"""
Auto-update the YouTube Shorts section on index.html from the channel's RSS feed.
Run manually or via the daily GitHub Action. Replaces:
  - The video cards between <!-- SHORTS-GRID-START --> and <!-- SHORTS-GRID-END -->
  - The VideoObject schema blocks between <!-- VIDEO-SCHEMA-START --> and <!-- VIDEO-SCHEMA-END -->
Only uses the Python standard library.
"""
import html
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET

CHANNEL_ID = "UC7RxbjYZ8iCNfsXBUYpmAsA"
FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
PAGE = "index.html"
MAX_VIDEOS = 6

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch_videos():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    root = ET.fromstring(data)
    videos = []
    for entry in root.findall("atom:entry", NS)[:MAX_VIDEOS]:
        vid = entry.find("yt:videoId", NS).text.strip()
        title = entry.find("media:group/media:title", NS).text.strip()
        published = entry.find("atom:published", NS).text.strip()[:10]
        stats = entry.find("media:group/media:community/media:statistics", NS)
        views = int(stats.get("views", "0")) if stats is not None else 0
        videos.append({"id": vid, "title": title, "published": published, "views": views})
    return videos


def fmt_views(v):
    if v >= 1_000_000:
        return f"{v / 1_000_000:.1f}M views"
    if v >= 1_000:
        return f"{v / 1_000:.1f}K views"
    return f"{v} views"


def build_cards(videos):
    cards = []
    for v in videos:
        t = html.escape(v["title"], quote=True)
        cards.append(
            f'      <div class="yt-card"><div class="yt-embed"><iframe src="https://www.youtube.com/embed/{v["id"]}" '
            f'title="{t}" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
            f'allowfullscreen></iframe></div><div class="yt-info"><h3>{t}</h3>'
            f'<div class="yt-views">{fmt_views(v["views"])}</div></div></div>'
        )
    return "\n".join(cards)


def build_schema(videos):
    blocks = []
    for v in videos:
        obj = {
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": v["title"],
            "description": (
                f'{v["title"]} — real walk footage from Spare Human Services. '
                "Licensed & insured dog walking and pet sitting in Largo, FL & throughout "
                "Pinellas County. Book at sparehumanservices.com"
            ),
            "thumbnailUrl": f'https://i.ytimg.com/vi/{v["id"]}/hqdefault.jpg',
            "uploadDate": v["published"],
            "contentUrl": f'https://www.youtube.com/shorts/{v["id"]}',
            "embedUrl": f'https://www.youtube.com/embed/{v["id"]}',
        }
        blocks.append(
            '  <script type="application/ld+json">\n  '
            + json.dumps(obj, indent=2, ensure_ascii=False)
            + "\n  </script>"
        )
    return "\n".join(blocks)


def replace_between(text, start_marker, end_marker, content):
    i = text.index(start_marker) + len(start_marker)
    j = text.index(end_marker)
    return text[:i] + "\n" + content + "\n" + text[j:]


def main():
    videos = fetch_videos()
    if not videos:
        print("ERROR: no videos found in feed — aborting without changes.")
        sys.exit(1)

    with open(PAGE, encoding="utf-8") as f:
        text = f.read()

    for marker in ("SHORTS-GRID-START", "SHORTS-GRID-END", "VIDEO-SCHEMA-START", "VIDEO-SCHEMA-END"):
        if marker not in text:
            print(f"ERROR: marker {marker} missing from {PAGE}")
            sys.exit(1)

    text = replace_between(text, "<!-- SHORTS-GRID-START -->", "<!-- SHORTS-GRID-END -->", build_cards(videos))
    text = replace_between(text, "<!-- VIDEO-SCHEMA-START -->", "<!-- VIDEO-SCHEMA-END -->", build_schema(videos))

    with open(PAGE, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Updated with {len(videos)} videos:")
    for v in videos:
        print(f'  {v["published"]} | {v["id"]} | {fmt_views(v["views"])} | {v["title"]}')


if __name__ == "__main__":
    main()
