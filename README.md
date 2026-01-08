# Intersections
A tiny, bash-based static page generator for personal link sharing.

Demo: [atarity.github.io/intersections/](https://atarity.github.io/intersections/)

## Features
- **Automatic Title Fetching**: Uses `curl` and `xmllint` to grab `<title>` tags.
- **Interactive Editing**: Pre-fills a CLI prompt using `zsh`'s `vared` so you can tweak titles before saving.
- **Non-Interactive Mode**: Use the `-y` flag for automated/bulk additions.
- **RSS Feed**: Generates a valid `feed.xml` with XML-escaped content.

## Dependencies
- `bash, python3, curl` (`zsh` for interactive mode on MacOS)

## Usage
- Add a link (Interactive): `./intersections "https://snnkv.com" "This is a cool site."`
- Autoconfirm: `./intersections -y "https://diy-synths.snnkv.com" "This also worth to visit."`

## TODO
- support utf8 in fetched titles
- use notch area on ios
- OG picture (the same for RSS entries)
- Cleanup header tags: titles, sites, og, favicon, etc
