import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

WATCH = Path(__file__).resolve().parents[1] / ".claude/skills/babysit/scripts/watch.py"


class WatchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.log = self.dir / "app.log"
        self.state = self.dir / "state.json"
        self.log.write_text("")
        self.deadline = time.time() + 20

    def tearDown(self):
        self.tmp.cleanup()

    def args(self, *extra, deadline=None):
        return [sys.executable, str(WATCH), "--log", str(self.log), "--state", str(self.state),
                "--session-id", "test", "--deadline", str(deadline or self.deadline),
                "--interval", "0.05", *extra]

    def run_once(self, *extra, deadline=None):
        result = subprocess.run(self.args(*extra, deadline=deadline), capture_output=True,
                                text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_deduplicates_matching_lines(self):
        self.log.write_text("2026-01-01T10:00:00Z ERROR db down\ninfo ok\n"
                            "2026-01-01T10:00:05Z ERROR db down\n")
        batch = self.run_once("--from-start")
        self.assertEqual(batch["event"], "incidents")
        self.assertEqual(len(batch["items"]), 1)
        self.assertEqual(batch["items"][0]["count"], 2)
        self.assertIn("<time>", batch["items"][0]["sample"])

    def test_quiet_log_reaches_deadline(self):
        self.log.write_text("info ok\n")
        batch = self.run_once("--from-start", deadline=time.time() + 0.5)
        self.assertEqual(batch["event"], "deadline")
        self.assertEqual(batch["items"], [])
        self.assertTrue(batch["stopped"])

    def test_starts_at_end_of_file_by_default(self):
        self.log.write_text("ERROR old\n")
        batch = self.run_once(deadline=time.time() + 0.5)
        self.assertEqual(batch["items"], [])

    def test_critical_flag(self):
        self.log.write_text("FATAL out of memory\n")
        item = self.run_once("--from-start")["items"][0]
        self.assertTrue(item["critical"])

    def test_rotation_reports_gap(self):
        self.log.write_text("ERROR first\n")
        self.run_once("--from-start")
        self.log.unlink()
        self.log.write_text("ERROR second\n")
        batch = self.run_once("--from-start")
        kinds = [item.get("kind") for item in batch["items"]]
        self.assertIn("coverage_gap", kinds)
        self.assertTrue(any("second" in item.get("sample", "") for item in batch["items"]))

    def test_rejects_state_from_other_config(self):
        self.log.write_text("ERROR first\n")
        self.run_once("--from-start")
        result = subprocess.run(self.args("--from-start", "--pattern", "other"),
                                capture_output=True, text=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("another session", result.stderr)

    def test_follow_streams_batches_until_deadline(self):
        process = subprocess.Popen(self.args("--follow", "--cooldown", "0",
                                             deadline=time.time() + 3),
                                   stdout=subprocess.PIPE, text=True)
        stdout = process.stdout
        assert stdout is not None
        try:
            time.sleep(0.5)
            with self.log.open("a") as handle:
                handle.write("ERROR one\n")
            first = json.loads(stdout.readline())
            with self.log.open("a") as handle:
                handle.write("ERROR two\n")
            second = json.loads(stdout.readline())
            last = json.loads(stdout.readline())
            self.assertEqual(process.wait(timeout=10), 0)
        finally:
            process.kill()
            stdout.close()
        self.assertIn("one", first["items"][0]["sample"])
        self.assertIn("two", second["items"][0]["sample"])
        self.assertFalse(first["stopped"])
        self.assertEqual(last["event"], "deadline")


if __name__ == "__main__":
    unittest.main()
