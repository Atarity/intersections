# Intersections
A tiny static page generator for personal link sharing.

Demo: [atarity.github.io/intersections/](https://atarity.github.io/intersections/)

## Features
- **Automatic Title Fetching**
- **Non-Interactive Mode**: Use the `-y` flag for automated additions.
- **RSS Feed**: Generates a valid `feed.xml` with XML-escaped content.

## Dependencies
- `python3` with standard libs

## Usage
- Add a link (Interactive): `python3 intersections.py "https://snnkv.com" "This is a cool site."`
- Autoconfirm: `python3 intersections.py -y "https://diy-synths.snnkv.com" "This also worth to visit."`

## TODO
- OG picture (the same for RSS entries)
- Cleanup header tags: titles, sites, og, favicon, etc
