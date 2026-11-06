import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

SVGL = Path(__file__).resolve().parents[1] / ".claude/skills/svgl/scripts/svgl.sh"

# Stand-in for curl: logs the URL, returns FAKE_BODY and FAKE_CODE like `-w`/`-o` would.
FAKE_CURL = r"""#!/usr/bin/env bash
out=""; fmt=""; url=""
while [ $# -gt 0 ]; do
  case "$1" in
    -o) out="$2"; shift 2 ;;
    -w) fmt="$2"; shift 2 ;;
    -A|--max-time) shift 2 ;;
    -*) shift ;;
    *) url="$1"; shift ;;
  esac
done
echo "$url" >> "$FAKE_LOG"
if [ -n "$out" ]; then cat "$FAKE_BODY" > "$out"; else cat "$FAKE_BODY"; fi
case "$fmt" in $'\n'*) printf '\n%s' "$FAKE_CODE" ;; *) printf '%s' "$FAKE_CODE" ;; esac
"""


class SvglTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        bin_dir = self.dir / "bin"
        bin_dir.mkdir()
        curl = bin_dir / "curl"
        curl.write_text(FAKE_CURL)
        curl.chmod(0o755)
        self.body = self.dir / "body"
        self.urls = self.dir / "urls"
        self.env = dict(os.environ, PATH=f"{bin_dir}:{os.environ['PATH']}",
                        FAKE_BODY=str(self.body), FAKE_LOG=str(self.urls), TMPDIR=str(self.dir))

    def tearDown(self):
        self.tmp.cleanup()

    def run_svgl(self, *args, body="", code="200"):
        self.body.write_text(body)
        return subprocess.run(["bash", str(SVGL), *args], capture_output=True, text=True,
                              env=dict(self.env, FAKE_CODE=code), timeout=30)

    def test_search_not_found_is_empty(self):
        result = self.run_svgl("search", "nothing", code="404")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [])

    def test_search_limits_client_side(self):
        logos = [{"title": name} for name in ("a", "b", "c")]
        result = self.run_svgl("search", "next js", "2", body=json.dumps(logos))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)), 2)
        url = self.urls.read_text().strip()
        self.assertIn("search=next%20js", url)
        self.assertNotIn("limit=", url)

    def test_search_rejects_non_json(self):
        result = self.run_svgl("search", "x", body="<html>challenge</html>")
        self.assertEqual(result.returncode, 1)
        self.assertIn("non-JSON", result.stderr)

    def test_download_saves_valid_svg(self):
        out = self.dir / "logos" / "x.svg"
        svg = '<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg"/>'
        result = self.run_svgl("download", "https://svgl.app/x.svg", str(out), body=svg)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(out.read_text(), svg)
        self.assertEqual(stat.S_IMODE(out.stat().st_mode), 0o644)

    def test_download_keeps_existing_file_on_bad_content(self):
        out = self.dir / "x.svg"
        out.write_text("good")
        for body, code in (('<?xml version="1.0"?><html/>', "200"), ("<svg", "200"),
                           ("<svg/>", "404")):
            result = self.run_svgl("download", "https://svgl.app/x.svg", str(out),
                                   body=body, code=code)
            self.assertEqual(result.returncode, 1, body)
            self.assertEqual(out.read_text(), "good")


if __name__ == "__main__":
    unittest.main()
