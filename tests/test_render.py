"""Exercise the build CLI in isolated directories, using the real JS renderer."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BuildCheckTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        for name in ("render.py", "script.js"):
            shutil.copyfile(ROOT / name, self.root / name)
        (self.root / "papers").mkdir()
        self.data = self.root / "papers/publications.json"
        self.data.write_text(json.dumps([{
            "title": "Example paper", "authors": ["Fan Yang"],
            "venue": "Example venue", "year": 2026,
            "link": "https://example.com/paper"
        }]), encoding="utf-8")
        self.source = self.root / "js_index.html"
        self.source.write_text(
            '<!DOCTYPE html><html><body><div id="paper-list" data-state="loading">'
            '<p>Loading publications…</p></div><script src="script.js"></script>'
            '</body></html>\n', encoding="utf-8"
        )
        self.sitemap = self.root / "sitemap.xml"
        self.sitemap.write_text('<urlset><url><lastmod>2000-01-01</lastmod></url></urlset>', encoding="utf-8")
        result = self.run_build()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.index = self.root / "index.html"

    def run_build(self, *args):
        return subprocess.run(
            [sys.executable, str(self.root / "render.py"), *args],
            capture_output=True, text=True, encoding="utf-8"
        )

    def snapshot(self):
        return {
            str(path.relative_to(self.root)): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in self.root.rglob("*") if path.is_file()
        }

    def test_check_accepts_current_page_without_writing_or_refreshing_sitemap(self):
        self.sitemap.write_text('<urlset><url><lastmod>2000-01-01</lastmod></url></urlset>', encoding="utf-8")
        before = self.snapshot()
        result = self.run_build("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_check_rejects_stale_page_without_rebuilding_it(self):
        self.source.write_text(self.source.read_text(encoding="utf-8").replace(
            "<body>", "<body><h1>Updated biography</h1>"
        ), encoding="utf-8")
        before = self.snapshot()
        result = self.run_build("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("python render.py", result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_check_rejects_missing_page_without_creating_it(self):
        self.index.unlink()
        before = self.snapshot()
        result = self.run_build("--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_publications_preserve_previous_outputs(self):
        papers = json.loads(self.data.read_text(encoding="utf-8"))
        papers[0]["link"] = "javascript:alert(1)"
        self.data.write_text(json.dumps(papers), encoding="utf-8")
        before = self.snapshot()
        for args in ((), ("--check",)):
            with self.subTest(args=args):
                result = self.run_build(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.snapshot(), before)

    def test_missing_placeholder_preserves_previous_outputs(self):
        self.source.write_text("<!DOCTYPE html><html><body></body></html>", encoding="utf-8")
        before = self.snapshot()
        for args in ((), ("--check",)):
            with self.subTest(args=args):
                result = self.run_build(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.snapshot(), before)


if __name__ == "__main__":
    unittest.main()
