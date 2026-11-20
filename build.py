"""Validate and assemble the standalone SIGNAL showcase for GitHub Pages."""

import argparse
import shutil
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


PUBLIC_FILES = {
    "index.html",
    "style.css",
    "gallery.js",
    "assets/signal.svg",
    "assets/today.jpg",
    "assets/intelligence.jpg",
    "assets/radar.jpg",
    "assets/ecosystem.jpg",
    "assets/research.jpg",
    "assets/dossier.jpg",
    "assets/social.jpg",
}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = set()
        self.references = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            self.targets.add(data["id"])
        self.references.extend(data[name] for name in ("href", "src") if name in data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="A new static output directory")
    args = parser.parse_args()
    source = Path(__file__).parent / "site"
    entries = list(source.rglob("*"))
    if any(path.is_symlink() for path in entries):
        parser.error("The public tree contains a symlink.")
    files = {path.relative_to(source).as_posix() for path in entries if path.is_file()}
    if files != PUBLIC_FILES:
        parser.error(f"Unexpected static inputs: {sorted(files ^ PUBLIC_FILES)}")
    page = Page()
    page.feed((source / "index.html").read_text(encoding="utf-8"))
    for ref in page.references:
        url = urlsplit(ref)
        if url.scheme == "https" and url.netloc:
            continue
        if url.scheme or url.netloc or url.path.startswith("/") or (url.path and url.path not in files):
            parser.error(f"Invalid or missing local reference: {ref}")
        if url.fragment and url.fragment not in page.targets:
            parser.error(f"Unknown navigation target: {ref}")
    if args.output.exists():
        parser.error("Choose a new output directory.")
    args.output.mkdir(parents=True)
    for name in sorted(files):
        destination = args.output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, destination)
    (args.output / ".nojekyll").touch()
    print(f"Built {len(files)} static files.")


if __name__ == "__main__":
    main()
