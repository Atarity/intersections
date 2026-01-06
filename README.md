# Intersections

A tiny, bash-based static site generator for personal link aggregators (like a private Google Reader).

## Features

- **Automatic Title Fetching**: Uses `curl` and `xmllint` to grab `<title>` tags.
- **Interactive Editing**: Pre-fills a CLI prompt using `zsh`'s `vared` so you can tweak titles before saving.
- **Non-Interactive Mode**: Use the `-y` flag for automated/bulk additions.
- **RSS Feed**: Generates a valid `feed.xml` with XML-escaped content.
- **Responsive Design**: Minimal CSS with a clean, high-contrast visual hierarchy and a 70x70 rounded avatar.

## Dependencies

- `bash` (or any POSIX shell)
- `curl` (for fetching pages)
- `xmllint` (usually part of `libxml2`, for robust HTML parsing)
- `zsh` (required for the interactive title editor on macOS)

## Usage

### Add a link (Interactive)
```bash
./intersections "https://example.com" "This is a cool site."
```
1. Script fetches the title.
2. CLI prompts: `Edit title: Example Domain`.
3. Press **Enter** to keep, or edit and press **Enter** to save.

### Add a link (Auto-confirm)
```bash
./intersections -y "https://example.com" "No prompt needed."
```

## Structure

- `intersections`: The core logic script.
- `index.html`: The generated homepage.
- `feed.xml`: The RSS 2.0 feed.
- `meta/`:
    - `main.css`: The styling logic.
    - `header.htm` / `footer.htm`: Header and footer snippets.
    - `timeline.htm`: The raw collection of entry snippets.
    - `rss_timeline.tmpl`: The raw collection of RSS items.
    - `rss_header.tmpl`: The XML structure for the feed header.
    - `avatar-bl.svg`: The default profile avatar.

## Development & Hosting

Since this generates raw HTML/XML, you can host it anywhere (GitHub Pages, Netlify, or a basic Nginx server). To test locally, just open `index.html` in your browser.
