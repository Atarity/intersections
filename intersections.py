#!/usr/bin/env python3
import argparse
import sys
import os
import re
import html
import subprocess
import urllib.request
import readline
from datetime import datetime

def fetch_title(url):
    """Fetch and extract page title using standard urllib and re."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            encoding = response.info().get_content_charset() or 'utf-8'
            content = response.read().decode(encoding, errors='ignore')
            m = re.search(r"(?i)<title[^>]*>(.*?)</title>", content, re.S)
            if m:
                # Basic cleanup: unescape entities and strip tags/excess space
                title = html.unescape(m.group(1).strip())
                title = re.sub(r'<[^>]*>', '', title)
                return title[:200]
    except Exception:
        pass
    return ""

def normalize_url(url):
    """Normalize URL by stripping protocol, www, and trailing slash."""
    url = re.sub(r'^https?://', '', url)
    url = re.sub(r'^www\.', '', url)
    return url.rstrip('/')

def main():
    parser = argparse.ArgumentParser(description="Intersections - A simple static site generator for links")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip interactive title edit")
    parser.add_argument("-l", "--local", action="store_true", help="Skip git integration")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("comment", nargs="?", default="", help="Optional comment")
    args = parser.parse_args()

    url_original = args.url
    comment = args.comment
    url_display = normalize_url(url_original)

    print(f"Fetching title for {url_original}...")
    page_title = fetch_title(url_original) or url_display

    if not args.yes:
        print(f"\nFetched title: {page_title}")
        # Add to history so Up Arrow works
        readline.add_history(page_title)
        try:
            new_title = input("[Enter] to confirm, [↑/↓] to edit: ").strip()
            if new_title:
                page_title = new_title
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            sys.exit(1)

    ts = datetime.now().strftime('%Y-%m-%d')
    rss_date = datetime.now().astimezone().strftime('%a, %d %b %Y %H:%M:%S %z')

    # HTML Snippet
    comment_html = ""
    if comment:
        comment_html = (
            "  <div class='comment-wrapper'>\n"
            "    <div class='avatar'><img src='meta/avatar-bl.svg' alt=''></div>\n"
            f"    <p class='comment'>{html.escape(comment)}</p>\n"
            "  </div>\n"
        )

    article_html = (
        f"<article id='{url_display}'>\n"
        "  <div class='entry-header'>\n"
        f"    <span class='ts'>{ts}</span>\n"
        f"    <h2 class='entry-title'><a href='{url_original}' target='_blank'>{html.escape(page_title)}</a></h2>\n"
        f"    <a href='{url_original}' class='url' target='_blank'>{url_display}</a>\n"
        "  </div>\n"
        f"{comment_html}"
        "</article>\n"
    )

    # File paths
    timeline_path = "meta/timeline.htm"
    rss_path = "meta/rss_timeline.tmpl"

    # Read existing timeline
    timeline_content = ""
    if os.path.exists(timeline_path):
        with open(timeline_path, "r", encoding="utf-8") as f:
            timeline_content = f.read()

    # Prepend and save timeline
    with open(timeline_path, "w", encoding="utf-8") as f:
        f.write(article_html + timeline_content)

    # Reassemble index.html
    with open("meta/header.htm", "r", encoding="utf-8") as f: header = f.read()
    with open("meta/footer.htm", "r", encoding="utf-8") as f: footer = f.read()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(header + article_html + timeline_content + footer)

    # RSS Item
    rss_item = (
        "<item>\n"
        f"  <title>{html.escape(page_title)}</title>\n"
        f"  <link>{html.escape(url_original)}</link>\n"
        f"  <description>{html.escape(comment)}</description>\n"
        f"  <pubDate>{rss_date}</pubDate>\n"
        f"  <guid>{html.escape(url_original)}</guid>\n"
        "</item>\n"
    )

    # Read existing RSS timeline
    rss_content = ""
    if os.path.exists(rss_path):
        with open(rss_path, "r", encoding="utf-8") as f:
            rss_content = f.read()

    # Prepend and save RSS timeline
    with open(rss_path, "w", encoding="utf-8") as f:
        f.write(rss_item + rss_content)

    # Reassemble feed.xml (Top 20 items)
    with open("meta/rss_header.tmpl", "r", encoding="utf-8") as f: rss_header = f.read()

    # Extract items from updated content
    all_items = re.findall(r'<item>.*?</item>', rss_item + rss_content, re.S)
    top_items = "\n".join(all_items[:20])

    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(rss_header)
        f.write(f"\n  <lastBuildDate>{rss_date}</lastBuildDate>\n")
        f.write(top_items)
        f.write("\n</channel>\n</rss>\n")

    print("-------")
    print(f"Title: {page_title}")
    print(f"Link added: {url_display}")
    print(f"Comment: {comment}")

    # Git integration
    if not args.local and os.path.isdir(".git"):
        subprocess.run(["git", "status", "--short"])
        subprocess.run(["git", "add", "-A"])
        subprocess.run(["git", "commit", "-m", f"Add link: {url_display}"])
        subprocess.run(["git", "push"])

if __name__ == "__main__":
    main()