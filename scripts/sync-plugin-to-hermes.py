#!/usr/bin/env python3
"""Synchronize the reviewed ModernUO plugin payload into a Hermes skill profile."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


REMOVED_PLUGIN_SKILLS = {
    "modernuo-issue-review",
    "rebirthuo-implement",
    "rebirthuo-implementation",
    "rebirthuo-implementation-checkpoints",
    "rebirthuo-issue-create",
    "rebirthuo-issue-review",
    "rebirthuo-modernuo-codebase",
    "rebirthuo-review-patterns",
    "uo-era-product-timeline",
    "uo-era-publish-source-gate",
    "uo-modernuo-workflow",
    "uo-product-model",
}


def skill_name(skill_md: Path) -> str | None:
    match = re.search(
        r"(?m)^name:\s*([^#\r\n]+)", skill_md.read_text(encoding="utf-8")
    )
    return match.group(1).strip().strip("\"'") if match else None


def hermes_map(root: Path) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for skill_md in root.rglob("SKILL.md"):
        name = skill_name(skill_md)
        if name:
            mapping[name] = skill_md.parent
    return mapping


def assert_within(path: Path, root: Path) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Refusing to modify path outside Hermes root: {path}") from exc


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin-skills",
        type=Path,
        default=repo_root / "plugins" / "modernuo" / "skills",
    )
    parser.add_argument(
        "--hermes-root",
        type=Path,
        required=True,
        help="Hermes profile skills directory to update",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--remove-orphans",
        action="store_true",
        help="Remove retired plugin skills found under the Hermes root",
    )
    parser.add_argument(
        "--skill",
        action="append",
        dest="skills",
        help="Sync only this skill name; may be repeated",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    plugin_root = args.plugin_skills.resolve()
    hermes_root = args.hermes_root.resolve()
    if not plugin_root.is_dir():
        raise SystemExit(f"Plugin skill root does not exist: {plugin_root}")
    if not hermes_root.is_dir():
        raise SystemExit(f"Hermes skill root does not exist: {hermes_root}")

    requested = set(args.skills or [])
    sources = {
        skill_dir.name: skill_dir
        for skill_dir in plugin_root.iterdir()
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists()
    }
    missing = sorted(requested - sources.keys())
    if missing:
        raise SystemExit(f"Unknown plugin skills: {', '.join(missing)}")

    destinations = hermes_map(hermes_root)
    orphans = sorted(REMOVED_PLUGIN_SKILLS.intersection(destinations))
    for name in orphans:
        destination = destinations[name]
        assert_within(destination, hermes_root)
        if args.remove_orphans and not args.dry_run:
            shutil.rmtree(destination)
            print(f"removed retired skill {name} -> {destination}")
        else:
            print(f"orphan cleanup required {name} -> {destination}")
    selected = sorted(requested or sources.keys())
    for name in selected:
        source = sources[name]
        destination = destinations.get(name, hermes_root / "software-development" / name)
        assert_within(destination, hermes_root)
        action = "would sync" if args.dry_run else "synced"
        if not args.dry_run:
            if destination.exists():
                shutil.rmtree(destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, destination)
            copied_name = skill_name(destination / "SKILL.md")
            if copied_name != name:
                raise RuntimeError(
                    f"Post-copy identity mismatch for {destination}: {copied_name!r}"
                )
        print(f"{action} {name} -> {destination}")

    print(f"{action} {len(selected)} skill(s)")


if __name__ == "__main__":
    main()
