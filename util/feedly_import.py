# below is "vibe-coded" massively. I didn't check the line, but it does import properly.

import os
import re
import html
from datetime import datetime

# Path to the exported starred.html
FILE_PATH = "starred.html"
# Cutoff year
MIN_YEAR = 2023
# Unix timestamp for 2023-01-01 00:00:00 UTC
MIN_TS = 1672531200

def xml_escape(text):
    if not text:
        return ""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")

def normalize_url(url):
    # Strip protocol and www
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)
    url = url.rstrip('/')
    return url

def process():
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found.")
        return

    print(f"Reading {FILE_PATH}...")
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find links: <DT><A HREF="..." ADD_DATE="...">...</A>
    pattern = re.compile(r'<DT><A HREF="(.*?)" ADD_DATE="(.*?)">(.*?)</A>', re.IGNORECASE)
    matches = pattern.findall(content)

    entries = []
    for url_original, ts_str, title_html in matches:
        try:
            ts = int(ts_str)
        except ValueError:
            continue

        if ts < MIN_TS:
            continue

        dt = datetime.utcfromtimestamp(ts)
        title = html.unescape(title_html)
        url_display = normalize_url(url_original)

        entries.append({
            'ts': ts,
            'date_str': dt.strftime('%Y-%m-%d'),
            'rss_date': dt.strftime('%a, %d %b %Y %H:%M:%S +0000'),
            'url_original': url_original,
            'url_display': url_display,
            'title': title
        })

    # Sort newest first
    entries.sort(key=lambda x: x['ts'], reverse=True)

    # Prepare snippets
    timeline_content = ""
    rss_content = ""

    for e in entries:
        # Intersections HTML schema
        timeline_content += f"""<article id='{e['url_display']}'>
  <div class='entry-header'>
    <span class='ts'>{e['date_str']}</span>
    <h2 class='entry-title'><a href='{e['url_original']}' target='_blank'>{e['title']}</a></h2>
    <a href='{e['url_original']}' class='url' target='_blank'>{e['url_display']}</a>
  </div>
</article>
"""
        # Intersections RSS schema
        rss_page_title = xml_escape(e['title'])
        rss_url_original = xml_escape(e['url_original'])

        rss_content += f"""<item>
  <title>{rss_page_title}</title>
  <link>{rss_url_original}</link>
  <description></description>
  <pubDate>{e['rss_date']}</pubDate>
  <guid>{rss_url_original}</guid>
</item>
"""

    with open('meta/timeline.htm', 'w', encoding='utf-8') as f:
        f.write(timeline_content)

    with open('meta/rss_timeline.tmpl', 'w', encoding='utf-8') as f:
        f.write(rss_content)

    print(f"Successfully imported {len(entries)} entries from {FILE_PATH} (starting from {MIN_YEAR}).")

if __name__ == "__main__":
    process()
