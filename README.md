# Intersections
A tiny static page generator for personal link sharing.

Demo: [https://intersections.snnkv.com/](https://intersections.snnkv.com/)

## Features
- Automatic Title Fetching
- RSS Feed: Generates a valid `feed.xml` with XML-escaped content.

## Dependencies
- `python3` with standard libs

## Usage
```bash
python3 intersections.py 'https://snnkv.com' 'This is a cool site.'
```
- **Single ticks are required** for most modern shells to avoid special characters expansion like `!`.
- `-y` is for non-interactive, automatic mode (submit without title editing)
- `-l` is for local mode (disable git commit-push)

## TODO
- Search bar
- TBD: Semantic tagging (as part of the page fetching)
