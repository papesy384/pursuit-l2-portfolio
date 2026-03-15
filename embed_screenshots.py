#!/usr/bin/env python3
"""Embed screenshot images as base64 data URIs in README.md."""
import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
README = ROOT / "README.md"

# file -> (mime, alt text)
IMAGES = [
    ("project1-slack.png", "image/jpeg", "Slack Smart-Notification Onboarding"),
    ("project2-icloud-notes.png", "image/jpeg", "iCloud Notes Web Clone"),
    ("project3-social-sofa.png", "image/png", "The Social Sofa"),
    ("project4-heat-tracker.png", "image/png", "Heat Tracker"),
    ("project5-aerostress.png", "image/jpeg", "AeroStress Dashboard"),
]

def main():
    text = README.read_text()
    for filename, mime, alt in IMAGES:
        path = ASSETS / filename
        if not path.exists():
            print(f"Skip (missing): {filename}")
            continue
        b64 = base64.b64encode(path.read_bytes()).decode("ascii")
        data_uri = f"data:{mime};base64,{b64}"
        # Replace ![alt](assets/filename) with embedded version
        pattern = r'!\[([^\]]*)\]\(assets/' + re.escape(filename) + r'\)'
        replacement = f"![{alt}]({data_uri})"
        new_text, n = re.subn(pattern, replacement, text, count=1)
        if n:
            text = new_text
            print(f"Embedded: {filename}")
        else:
            print(f"No match: {filename}")
    README.write_text(text)
    print("Done. README size:", README.stat().st_size)

if __name__ == "__main__":
    main()
