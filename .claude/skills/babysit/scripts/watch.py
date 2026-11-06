#!/usr/bin/env python3
"""Quiet incident filter: runs a source command (or reads stdin), one JSON event per stdout line."""
import argparse
import hashlib
import json
import os
import re
import select
import signal
import subprocess
import sys
import time


def normalize(line):
    line = re.sub(r"\x1b\[[0-9;]*m", "", line)
    line = re.sub(r"\b\d{4}-\d\d-\d\d[T ][\d:.,]+(?:Z|[+-]\d\d:?\d\d)?", "<time>", line)
    line = re.sub(r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b", "<uuid>", line, flags=re.I)
    line = re.sub(r"\b(?:0x)?[0-9a-f]{12,}\b", "<hex>", line, flags=re.I)
    line = re.sub(r"\d+", "<n>", line)
    return " ".join(line.split())


def emit(event, **fields):
    print(json.dumps({"event": event, **fields}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deadline", type=float, required=True, help="Unix timestamp")
    parser.add_argument("--pattern", default=r"\b(error|exception|failed|fatal|panic|critical|traceback)\b")
    parser.add_argument("--critical", default=r"\b(critical|fatal|panic)\b")
    parser.add_argument("--cooldown", type=float, default=60, help="seconds between repeat reports")
    parser.add_argument("--max-signatures", type=int, default=256)
    parser.add_argument("--once", action="store_true", help="exit after the first events")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="-- SOURCE COMMAND; stdin when omitted")
    args = parser.parse_args()
    if args.deadline > time.time() + 86400:
        parser.error("deadline must be within 24 hours")
    pattern, critical = re.compile(args.pattern, re.I), re.compile(args.critical, re.I)
    seen = {}
    overflow = False
    emitted = False

    def report(event, **fields):
        nonlocal emitted
        emitted = True
        emit(event, **fields)

    def flush(force=False):
        now = time.time()
        for signature, item in seen.items():
            if item["pending"] and (force or now - item["last"] >= args.cooldown):
                report("repeat", signature=signature, sample=item["sample"],
                       count=item["pending"], critical=item["critical"])
                item.update(pending=0, last=now)

    def handle(raw):
        nonlocal overflow
        line = raw.decode("utf-8", errors="replace").rstrip("\r")
        severe = bool(critical.search(line))
        if not severe and not pattern.search(line):
            return
        signature = hashlib.sha256(normalize(line).encode()).hexdigest()[:16]
        sample = " ".join(line.split())[:240]
        item = seen.get(signature)
        if item is None and len(seen) >= args.max_signatures:
            if not overflow:
                overflow = True
                report("overflow", detail="signature limit reached; only critical lines are reported now")
            if severe:
                report("incident", signature=signature, sample=sample, critical=True)
            return
        if item is None:
            seen[signature] = {"sample": sample, "pending": 0, "last": time.time(), "critical": severe}
            report("incident", signature=signature, sample=sample, critical=severe)
        elif severe and not item["critical"]:
            item.update(critical=True, last=time.time())
            report("incident", signature=signature, sample=sample, critical=True)
        else:
            item["pending"] += 1

    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    child = (subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, start_new_session=True) if command else None)
    try:
        watch(child.stdout.fileno() if child else sys.stdin.fileno(), args, handle, flush, lambda: emitted)
    finally:
        if child and child.poll() is None:
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try:
                    os.killpg(child.pid, sig)
                    child.wait(timeout=5)
                    break
                except ProcessLookupError:
                    break
                except subprocess.TimeoutExpired:
                    continue


def watch(fd, args, handle, flush, emitted):
    partial = b""
    while True:
        remaining = args.deadline - time.time()
        if remaining <= 0:
            flush(force=True)
            emit("deadline")
            return
        if select.select([fd], [], [], min(1.0, remaining))[0]:
            chunk = os.read(fd, 65536)
            if not chunk:
                if partial:
                    handle(partial)
                flush(force=True)
                emit("eof", detail="source ended; nothing is being watched")
                return
            lines = (partial + chunk).split(b"\n")
            partial = lines.pop()
            if len(partial) > 65536:
                lines.append(partial)
                partial = b""
            for raw in lines:
                handle(raw)
        flush()
        if args.once and emitted():
            return


if __name__ == "__main__":
    main()
