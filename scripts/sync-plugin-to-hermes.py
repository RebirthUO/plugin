#!/usr/bin/env python3
"""Preview or synchronize reviewed ModernUO skills to an explicit Hermes profile."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hermes-root", type=Path, required=True)
    parser.add_argument("--skill", action="append")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    source_root = repo / "plugins" / "modernuo" / "skills"
    target_root = args.hermes_root.resolve()
    if not target_root.is_dir():
        raise SystemExit(f"Hermes root does not exist: {target_root}")
    names = args.skill or sorted(p.name for p in source_root.iterdir() if (p / "SKILL.md").is_file())
    for name in names:
        source = source_root / name
        target = target_root / "modernuo" / name
        if not (source / "SKILL.md").is_file() or not within(target, target_root):
            raise SystemExit(f"Invalid skill or target: {name}")
        action = "would sync" if args.dry_run else "sync"
        print(f"{action}: {source} -> {target}")
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
