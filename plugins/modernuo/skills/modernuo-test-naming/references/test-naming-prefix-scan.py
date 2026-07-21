#!/usr/bin/env python3
"""Report actionable synthetic prefixes beneath a repository-relative test root."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: test-naming-prefix-scan.py <test-root>")

    root = Path.cwd().resolve()
    tests = Path(sys.argv[1]).resolve()
    if not tests.is_dir():
        raise SystemExit(f"test root does not exist or is not a directory: {tests}")
    try:
        tests.relative_to(root)
    except ValueError:
        raise SystemExit(f"test root must be below repository root {root}: {tests}")
    hard = re.compile(r"^(Publish\d+|Pub\d+|P\d+|Issue\d+|Task\d+|Codex|Generated|Regression|AI)")
    generic = re.compile(r"(Coverage|Smoke)")
    method_prefix = re.compile(
        r"(?:public|private|internal|protected)\s+(?:static\s+)?(?:async\s+)?(?:void|Task|ValueTask)\s+"
        r"((?:MondainsLegacy|SamuraiEmpire|Publish\d+|Pub\d+|P\d+|Issue\d+|Task\d+|Codex|Generated|Regression|AI)[A-Za-z0-9_]*)\s*\("
    )
    hard_remaining: list[tuple[str, str, str]] = []
    soft_candidates: list[tuple[str, str, str]] = []
    for path in sorted(tests.rglob("*.cs")):
        relative = path.relative_to(root).as_posix()
        if hard.match(path.stem):
            hard_remaining.append(("file", relative, path.stem))
        elif generic.search(path.stem):
            soft_candidates.append(("file", relative, path.stem))
        text = path.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"\bclass\s+([A-Za-z0-9_]+)", text):
            name = match.group(1)
            if hard.match(name):
                hard_remaining.append(("class", relative, name))
            elif generic.search(name):
                soft_candidates.append(("class", relative, name))
        for match in method_prefix.finditer(text):
            name = match.group(1)
            if "SourceReferenceTests.cs" in relative or relative.endswith("MLSetArmorTests.cs"):
                continue
            hard_remaining.append(("method", relative, name))
    print(f"hard={len(hard_remaining)} soft={len(soft_candidates)}")
    for row in hard_remaining:
        print(row)
    for row in soft_candidates:
        print(("SOFT", *row))


if __name__ == "__main__":
    main()
