#!/usr/bin/env python3
"""Check or normalize generated metadata for one or more ModernUO skills."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"{path}: invalid YAML frontmatter")
    data = yaml.safe_load(parts[1])
    if not isinstance(data, dict):
        raise ValueError(f"{path}: frontmatter must be a mapping")
    return data


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", help="skill name; repeatable")
    args = parser.parse_args()
    skills_root = root / "plugins" / "modernuo" / "skills"
    selected = args.skill or [p.name for p in skills_root.iterdir() if (p / "SKILL.md").is_file()]
    failures: list[str] = []
    for name in sorted(selected):
        skill = skills_root / name
        try:
            fm = frontmatter(skill / "SKILL.md")
            manifest = json.loads((skill / "manifest.json").read_text(encoding="utf-8"))
            interface = yaml.safe_load((skill / "agents" / "interface.yaml").read_text(encoding="utf-8"))
            version = str((fm.get("metadata") or {}).get("version", ""))
            if fm.get("name") != name or manifest.get("name") != name:
                failures.append(f"{name}: name mismatch")
            if not version or manifest.get("version") != version:
                failures.append(f"{name}: SKILL.md and manifest version mismatch")
            if not isinstance(interface, dict) or not interface.get("interface", {}).get("default_prompt"):
                failures.append(f"{name}: missing interface.default_prompt")
            for relative in ("evals/baseline_description.txt", "evals/trigger_cases.json", "evals/semantic_config.json"):
                if not (skill / relative).is_file():
                    failures.append(f"{name}: missing {relative}")
        except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
            failures.append(str(exc))
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"prepared-check: {len(selected)} skill(s) valid")


if __name__ == "__main__":
    main()
