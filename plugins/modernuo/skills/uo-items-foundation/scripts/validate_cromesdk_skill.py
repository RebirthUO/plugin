#!/usr/bin/env python3
"""Validate a CromeSDK-marked SKILL.md against the schema rules used
by RebirthUO personal skills.

Covers:
  * Frontmatter starts at byte 0 with `---` and closes with `\n---\n`.
  * Parses as a YAML mapping.
  * `name` (≤ 64 chars) and `description` (≤ 1024 chars) present.
  * Total file ≤ 100,000 chars.
  * CromeSDK ownership metadata present and well-formed
    (`metadata.cromesdk.sync.marker == 'cromesdk-personal-skill'`,
    `owner == 'Crome696'`, `plugin-allowed == True`).
  * Required tags include `cromesdk-personal-skill`, `cromesdk-sync-managed`,
    `plugin-allowed`.

Exit code 0 on success, 1 on first failure.

Usage:
    python3 validate_cromesdk_skill.py path/to/SKILL.md [more/SKILL.md ...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"not a file: {path}"]

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append("frontmatter does not start at byte 0")
        return errors
    m = re.search(r"\n---\s*\n", text[3:])
    if m is None:
        errors.append("frontmatter not closed with `\\n---\\n`")
        return errors

    if len(text) > 100_000:
        errors.append(f"file too large: {len(text)} chars (limit 100,000)")

    try:
        fm = yaml.safe_load(text[3 : m.start() + 3])
    except yaml.YAMLError as e:
        errors.append(f"frontmatter not valid YAML: {e}")
        return errors

    name = fm.get("name")
    if not isinstance(name, str) or not name:
        errors.append("`name` missing or empty")
    elif len(name) > 64:
        errors.append(f"`name` too long: {len(name)} chars (limit 64)")

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc:
        errors.append("`description` missing or empty")
    elif len(desc) > 1024:
        errors.append(f"`description` too long: {len(desc)} chars (limit 1024)")

    sync = fm.get("metadata", {}).get("cromesdk", {}).get("sync", {})
    if sync.get("marker") != "cromesdk-personal-skill":
        errors.append("`metadata.cromesdk.sync.marker` must be 'cromesdk-personal-skill'")
    if sync.get("owner") != "Crome696":
        errors.append("`metadata.cromesdk.sync.owner` must be 'Crome696'")
    if sync.get("plugin-allowed") is not True:
        errors.append("`metadata.cromesdk.sync.plugin-allowed` must be true")

    tags = fm.get("metadata", {}).get("hermes", {}).get("tags", [])
    for required in ("cromesdk-personal-skill", "cromesdk-sync-managed", "plugin-allowed"):
        if required not in tags:
            errors.append(f"`metadata.hermes.tags` missing required tag: {required}")

    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    rc = 0
    for raw in argv:
        path = Path(raw)
        errs = validate(path)
        if errs:
            rc = 1
            print(f"FAIL  {path}")
            for e in errs:
                print(f"      - {e}")
        else:
            print(f"OK    {path}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
