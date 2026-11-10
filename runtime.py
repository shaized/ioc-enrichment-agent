"""Local, dependency-free I/O for the security agent examples."""

from __future__ import annotations

import argparse
import html
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

MAX_INPUT_BYTES = 2 * 1024 * 1024


def obj(value, name):
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def rows(value, name):
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")
    return [obj(item, f"{name}[{i}]") for i, item in enumerate(value)]


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value.strip()


def choice(value, allowed, name):
    if not isinstance(value, str) or value not in allowed:
        raise ValueError(f"{name} must be one of {', '.join(allowed)}")
    return value


def number(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if not math.isfinite(value) or value < minimum:
        raise ValueError(f"{name} must be finite and at least {minimum}")
    return value


def integer(value, name, minimum=0):
    number(value, name, minimum)
    if not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def instant(value, name):
    raw = text(value, name)
    try:
        result = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{name} must be an ISO 8601 timestamp") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError(f"{name} must include a UTC offset")
    return result.astimezone(timezone.utc)


def utc(value):
    return value.isoformat().replace("+00:00", "Z")


def unique(items, key="id"):
    seen = set()
    for item in items:
        value = text(item.get(key), key)
        if value in seen:
            raise ValueError(f"duplicate {key}: {value}")
        seen.add(value)


def strings(value, name):
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list of strings")
    return [text(item, name) for item in value]


def report(agent, summary, findings, limitations, next_steps):
    return {
        "schema_version": "1.0",
        "agent": agent,
        "summary": summary,
        "findings": findings,
        "limitations": limitations,
        "next_steps": next_steps,
    }


def escape(value):
    if not isinstance(value, str):
        value = json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)
    value = html.escape(value, quote=False)
    for char in "\\`*_{}[]()#+.!|~":
        value = value.replace(char, "\\" + char)
    return value.replace("\r", " ").replace("\n", " ")


def markdown(result):
    lines = [f"# {escape(result['agent'])}", "", "## Summary", ""]
    lines.extend(
        f"- **{escape(k.replace('_', ' '))}:** {escape(v)}"
        for k, v in result["summary"].items()
    )
    lines.extend(["", "## Findings", ""])
    for i, finding in enumerate(result["findings"], 1):
        lines.extend([f"### Finding {i}", ""])
        lines.extend(
            f"- **{escape(k.replace('_', ' '))}:** {escape(v)}"
            for k, v in finding.items()
        )
        lines.append("")
    if not result["findings"]:
        lines.append("No findings in the supplied scope. See limitations.")
    for name in ("limitations", "next_steps"):
        lines.extend(["", f"## {name.replace('_', ' ').title()}", ""])
        lines.extend(f"- {escape(item)}" for item in result[name])
    return "\n".join(lines) + "\n"


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError("input exceeds the 2 MiB limit")
    return obj(json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs), "input")


def cli(analyze, description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input", help="Path to a local JSON evidence snapshot")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    try:
        result = analyze(load(args.input))
        output = (
            json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)
            if args.format == "json"
            else markdown(result)
        )
    except (ValueError, TypeError, KeyError, OSError, RecursionError) as exc:
        parser.exit(2, f"Invalid input: {exc}\n")
    sys.stdout.write(output.rstrip() + "\n")
