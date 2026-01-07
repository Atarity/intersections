# Intersections
A tiny, bash-based static page generator for personal link sharing.

## Features

- **Automatic Title Fetching**: Uses `curl` and `xmllint` to grab `<title>` tags.
- **Interactive Editing**: Pre-fills a CLI prompt using `zsh`'s `vared` so you can tweak titles before saving.
- **Non-Interactive Mode**: Use the `-y` flag for automated/bulk additions.
- **RSS Feed**: Generates a valid `feed.xml` with XML-escaped content.
- **Responsive Design**: Minimal CSS with a clean, high-contrast visual hierarchy and a 70x70 rounded avatar.

## Dependencies

- `bash` (`zsh` for interactive mode)
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
