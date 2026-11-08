#!/usr/bin/env python3
"""Stable CardLink reference formatter. No network, no credentials, no card writes."""
import argparse
import json
import re
import sys

ROOT = re.compile(r"^[A-Za-z0-9_-]+$")
REFERENCE = re.compile(r"^\[Card#ID/([A-Za-z0-9_-]+)#([^\]\n]+)\]$")


def build(root_id, label):
    root_id = (root_id or "").strip()
    label = (label or "").strip()
    if not ROOT.fullmatch(root_id):
        raise ValueError("root_id must be non-empty letters/digits/_-, without spaces")
    if not label or "]" in label or "\n" in label or "\r" in label:
        raise ValueError("label must be non-empty and must not contain ] or newlines")
    return f"[Card#ID/{root_id}#{label}]"


def check(value):
    match = REFERENCE.fullmatch((value or "").strip())
    if not match:
        raise ValueError("not a single valid [Card#ID/<root_id>#<label>] reference")
    return {"root_id": match.group(1), "label": match.group(2),
            "reference": match.group(0)}


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    ref = commands.add_parser("ref", help="build one reference")
    ref.add_argument("--root-id", required=True)
    ref.add_argument("--label", required=True)
    ref.add_argument("--json", action="store_true")
    check_cmd = commands.add_parser("check", help="validate one reference")
    check_cmd.add_argument("value")
    args = parser.parse_args(argv)
    try:
        if args.action == "ref":
            value = build(args.root_id, args.label)
            print(json.dumps({"reference": value}, ensure_ascii=False)
                  if args.json else value)
        else:
            print(json.dumps(check(args.value), ensure_ascii=False, indent=2))
        return 0
    except ValueError as error:
        print(json.dumps({"status": "error", "message": str(error)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
