import json
import subprocess
import sys
import time
import unittest
from pathlib import Path

WATCH = Path(__file__).resolve().parents[1] / ".claude/skills/babysit/scripts/watch.py"


def run(text, *extra, deadline=20):
    result = subprocess.run([sys.executable, str(WATCH), "--deadline", str(time.time() + deadline), *extra],
                            input=text, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    return [json.loads(line) for line in result.stdout.splitlines()]


class WatchTest(unittest.TestCase):
    def test_reports_new_incident_and_counts_repeats(self):
        events = run("2026-01-01T10:00:00Z ERROR db down after 3 retries\ninfo ok\n"
                     "2026-01-01T10:00:05Z ERROR db down after 4 retries\n"
                     "2026-01-01T10:00:09Z ERROR db down after 5 retries\n")
        self.assertEqual([e["event"] for e in events], ["incident", "repeat", "eof"])
        self.assertIn("db down", events[0]["sample"])
        self.assertEqual(events[1]["count"], 2)

    def test_ignores_normal_lines(self):
        self.assertEqual([e["event"] for e in run("info ok\nstarted\n")], ["eof"])

    def test_critical_escalates_known_signature(self):
        events = run("error worker stopped\nFATAL error worker stopped\n")
        self.assertEqual([e["critical"] for e in events if e["event"] == "incident"], [False, True])

    def test_last_line_without_newline(self):
        events = run("ERROR tail line")
        self.assertEqual(events[0]["event"], "incident")

    def test_overflow_keeps_critical_lines(self):
        events = run("ERROR alpha\nERROR beta\nERROR gamma\nFATAL delta\n", "--max-signatures", "2")
        kinds = [e["event"] for e in events]
        self.assertEqual(kinds.count("overflow"), 1)
        self.assertTrue(any(e.get("critical") and "delta" in e["sample"] for e in events))
        self.assertFalse(any("gamma" in e.get("sample", "") for e in events))

    def test_deadline_with_open_quiet_source(self):
        process = subprocess.Popen([sys.executable, str(WATCH), "--deadline", str(time.time() + 1)],
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        try:
            assert process.stdout is not None
            line = process.stdout.readline()
            self.assertEqual(json.loads(line)["event"], "deadline")
            self.assertEqual(process.wait(timeout=10), 0)
        finally:
            process.kill()
            for stream in (process.stdin, process.stdout):
                if stream:
                    stream.close()

    def test_streams_events_and_once_exits_after_first(self):
        process = subprocess.Popen([sys.executable, str(WATCH), "--deadline", str(time.time() + 10),
                                    "--once"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        try:
            assert process.stdin is not None and process.stdout is not None
            process.stdin.write("ERROR one\n")
            process.stdin.flush()
            self.assertIn("one", json.loads(process.stdout.readline())["sample"])
            self.assertEqual(process.wait(timeout=10), 0)
        finally:
            process.kill()
            for stream in (process.stdin, process.stdout):
                if stream:
                    stream.close()


    def test_runs_source_command_and_stops_it(self):
        started = time.time()
        events = run("", "--once", "--", "sh", "-c", "echo ERROR from child; exec sleep 30")
        self.assertIn("from child", events[0]["sample"])
        self.assertLess(time.time() - started, 10)
        self.assertEqual(subprocess.run(["pgrep", "-f", "exec sleep 30"]).returncode, 1)

    def test_command_exit_is_eof(self):
        events = run("", "--", "sh", "-c", "echo boom >&2; exit 3")
        self.assertEqual([e["event"] for e in events], ["eof"])

if __name__ == "__main__":
    unittest.main()
