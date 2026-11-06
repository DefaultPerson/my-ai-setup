#!/usr/bin/env python3
"""Bounded log filter. JSON batches on stdout; --follow streams them until the deadline."""
import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
import time


def normalize(line):
    line = re.sub(r"\x1b\[[0-9;]*m", "", line)
    line = re.sub(r"\b\d{4}-\d\d-\d\d[T ][\d:.]+(?:Z|[+-]\d\d:?\d\d)?", "<time>", line)
    line = re.sub(r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b", "<uuid>", line, flags=re.I)
    line = re.sub(r"\b((?:request|trace|correlation)[_-]?id[=: ]+)\S+", r"\1<id>", line, flags=re.I)
    return " ".join(line.split())


def save(path, state):
    fd, name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def gap(state, reason):
    if reason not in state["gaps"]:
        state["gaps"].append(reason)


def collect(args, state, pattern, critical):
    try:
        # O_NONBLOCK avoids hanging at open() on a mistakenly selected FIFO.
        with os.fdopen(os.open(args.log, os.O_RDONLY | os.O_NONBLOCK), "rb") as handle:
            info = os.fstat(handle.fileno())
            if not stat.S_ISREG(info.st_mode):
                raise OSError("source is not a regular file")
            identity = [info.st_dev, info.st_ino]
            cursor = state.get("cursor")
            if cursor is None:
                cursor = {"identity": identity, "offset": 0 if args.from_start else info.st_size,
                          "partial": "", "anchor": ""}
            else:
                cursor = dict(cursor)
            changed = cursor["identity"] != identity
            truncated = info.st_size < cursor["offset"]
            handle.seek(max(0, cursor["offset"] - 128))
            anchor = handle.read(min(128, cursor["offset"]))
            mismatch = bool(cursor["anchor"]) and base64.b64encode(anchor).decode() != cursor["anchor"]
            if changed or truncated or mismatch:
                gap(state, "rotation/truncation/anchor change; unread old bytes may be lost")
                if cursor["partial"]:
                    gap(state, "incomplete line discarded at source change")
                cursor.update(identity=identity, offset=0, partial="", anchor="")
            handle.seek(cursor["offset"])
            chunk = handle.read(1024 * 1024)
            cursor["offset"] += len(chunk)
            data = base64.b64decode(cursor["partial"]) + chunk
            lines = data.split(b"\n")
            partial = lines.pop()
            if len(partial) > 16384:
                gap(state, "oversized incomplete line discarded; narrow or sanitize source")
                partial = b""
            cursor["partial"] = base64.b64encode(partial).decode()
            handle.seek(max(0, cursor["offset"] - 128))
            cursor["anchor"] = base64.b64encode(handle.read(min(128, cursor["offset"]))).decode()
            backlog = max(0, os.fstat(handle.fileno()).st_size - cursor["offset"])
            if backlog and not state.get("backlog_alerted"):
                gap(state, "source backlog remains; later incidents not yet inspected")
            state.update(backlog_bytes_at_read=backlog, backlog_alerted=bool(backlog))
            state["cursor"] = cursor
            state["failures"] = 0
    except OSError as error:
        state["failures"] += 1
        gap(state, "source read failed: " + type(error).__name__)
        return
    for raw in lines:
        if len(raw) > 16384:
            gap(state, "oversized line skipped; narrow or sanitize source")
            continue
        line = raw.decode("utf-8", errors="replace")
        severe = bool(critical.search(line))
        if not severe and not pattern.search(line):
            continue
        sample = normalize(line)
        signature = hashlib.sha256(sample.encode()).hexdigest()[:16]
        incident = state["incidents"].get(signature)
        if incident is None:
            if len(state["incidents"]) >= 256:
                state["overflow"] = True
                gap(state, "signature limit reached; collection stopped, full log remains at source")
                break
            incident = {"signature": signature, "sample": sample[:240], "count": 0,
                        "pending": 0, "critical": severe, "sent_critical": False, "last_sent": None}
            state["incidents"][signature] = incident
        incident["count"] += 1
        incident["pending"] += 1
        incident["critical"] = incident["critical"] or severe


def report(args, state, ended=False):
    now = time.time()
    eligible = [item for item in state["incidents"].values() if item["pending"] and
                (ended or item["last_sent"] is None or now - item["last_sent"] >= args.cooldown or
                 (item["critical"] and not item["sent_critical"]))]
    eligible.sort(key=lambda item: not item["critical"])
    gaps = state["gaps"][:8]
    chosen = eligible[:8 - len(gaps)]
    if not chosen and not gaps and not ended:
        return False
    items = [{"kind": "coverage_gap", "detail": reason} for reason in gaps]
    del state["gaps"][:len(gaps)]
    for item in chosen:
        items.append({key: item[key] for key in ("signature", "sample", "count", "pending", "critical")})
        item.update(pending=0, last_sent=now, sent_critical=item["critical"])
    state["last_report"] = now
    save(args.state, state)
    print(json.dumps({"event": "deadline" if ended else "incidents", "log": str(args.log),
                      "state": str(args.state), "items": items, "failures": state["failures"],
                      "more": bool(state["gaps"] or len(eligible) > len(chosen)),
                      "pending_signatures": sum(bool(i["pending"]) for i in state["incidents"].values()),
                      "backlog_bytes_at_read": state.get("backlog_bytes_at_read"),
                      "incomplete_line": bool(state.get("cursor", {}).get("partial")),
                      "stopped": ended or state["failures"] >= 3 or state["overflow"]}), flush=True)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--deadline", type=float, required=True, help="fixed Unix timestamp")
    parser.add_argument("--from-start", action="store_true")
    parser.add_argument("--follow", action="store_true", help="keep emitting batches until deadline/stop")
    parser.add_argument("--pattern", default=r"\b(error|exception|failed|fatal|panic|critical)\b")
    parser.add_argument("--critical", default=r"\b(critical|fatal|panic)\b")
    parser.add_argument("--cooldown", type=float, default=60)
    parser.add_argument("--interval", type=float, default=1)
    args = parser.parse_args()
    if not (0.05 <= args.interval <= 60 and 0 <= args.cooldown <= 86400):
        parser.error("interval must be 0.05..60 seconds and cooldown 0..86400 seconds")
    if not math.isfinite(args.deadline) or args.deadline > time.time() + 86400:
        parser.error("deadline must be finite and within 24 hours")
    args.log = args.log.resolve()
    args.state = args.state.resolve()
    if args.log == args.state or (args.log.exists() and args.state.exists() and
                                  os.path.samefile(args.log, args.state)):
        parser.error("state cannot be the source")
    pattern, critical = re.compile(args.pattern, re.I), re.compile(args.critical, re.I)
    config = {"session_id": args.session_id, "log": str(args.log), "deadline": args.deadline,
              "pattern": args.pattern, "critical": args.critical, "cooldown": args.cooldown}
    state = json.loads(args.state.read_text()) if args.state.exists() else {
        "config": config, "incidents": {}, "gaps": [], "failures": 0, "overflow": False}
    if state["config"] != config:
        parser.error("state belongs to another session/source/config; start fresh explicitly")
    if state["overflow"] or state["failures"] >= 3:
        parser.error("collection stopped at its failure/signature limit; inspect state and source")
    monotonic_end = time.monotonic() + max(0, args.deadline - time.time())
    while True:
        remaining = min(args.deadline - time.time(), monotonic_end - time.monotonic())
        if remaining <= 0:
            report(args, state, ended=True)
            return
        collect(args, state, pattern, critical)
        if report(args, state) and (not args.follow or state["failures"] >= 3 or state["overflow"]):
            return
        save(args.state, state)
        if state.get("backlog_bytes_at_read"):
            continue  # Drain backlog without interval delays; deadline still checked per chunk.
        remaining = min(args.deadline - time.time(), monotonic_end - time.monotonic())
        time.sleep(max(0, min(args.interval, remaining)))


if __name__ == "__main__":
    main()
