"""Build the static page with the shared JS renderer; Python and Node.js only."""
from datetime import date
from pathlib import Path
import argparse
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="Validate publications and index.html without writing files; ignore sitemap dates."
    )
    args = parser.parse_args()
    data_path = ROOT / "papers/publications.json"
    expected_count = len(json.loads(data_path.read_text(encoding="utf-8")))
    # Execute the same renderer used by the editable page, without a browser.
    result = subprocess.run(
        ["node", str(ROOT / "script.js"), str(data_path)],
        check=True, capture_output=True, text=True, encoding="utf-8"
    )
    if result.stdout.count("<li>") != expected_count:
        raise RuntimeError("Publication count mismatch; index.html was not updated.")
    source = (ROOT / "js_index.html").read_text(encoding="utf-8")
    replacement = (
        f'<div id="paper-list" data-state="ready" data-count="{expected_count}">\n'
        + result.stdout + "\n</div>"
    )
    output, count = re.subn(
        r'<div id="paper-list" data-state="loading">.*?</div>',
        lambda match: replacement, source, count=1, flags=re.DOTALL
    )
    if count != 1:
        raise RuntimeError("Publication placeholder missing; index.html was not updated.")
    output = re.sub(r'\s*<script src="script\.js"></script>', "", output)
    output = re.sub(r'\s*<noscript>.*?</noscript>', "", output, flags=re.DOTALL)
    if args.check:
        index = ROOT / "index.html"
        if not index.exists() or index.read_text(encoding="utf-8") != output:
            parser.exit(
                1, "index.html is missing or out of date. Run 'python render.py' "
                "and commit the generated page.\n"
            )
        # The sitemap date changes with normal builds, not with source validity.
        print(f"Validated {expected_count} publications; index.html is up to date. No files changed.")
        return
    temporary = ROOT / "index.html.tmp"
    temporary.write_text(output, encoding="utf-8")
    temporary.replace(ROOT / "index.html")

    sitemap = ROOT / "sitemap.xml"
    if sitemap.exists():
        content = sitemap.read_text(encoding="utf-8")
        content = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{date.today().isoformat()}</lastmod>", content)
        sitemap.write_text(content, encoding="utf-8")
    print(f"Built index.html with {expected_count} publications; sitemap updated.")


if __name__ == "__main__":
    main()
