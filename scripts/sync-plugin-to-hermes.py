#!/usr/bin/env python3
"""Copy updated plugin skills back to Hermes source paths."""

import re
import shutil
from pathlib import Path

HERMES_ROOT = Path(r"C:\Users\Jsiem\AppData\Local\hermes\profiles\ultima-online\skills")
PLUGIN_SKILLS = Path(r"C:\Users\Jsiem\Documents\GitHub\RebirthUO\plugin\plugins\modernuo\skills")


def hermes_map() -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    for skill_md in HERMES_ROOT.rglob("SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        m = re.search(r"(?m)^name:\s*(.+)$", text)
        if m:
            mapping[m.group(1).strip().strip('"').strip("'")] = skill_md.parent
    return mapping


def main() -> None:
    hmap = hermes_map()
    for skill_dir in sorted(PLUGIN_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        name = skill_dir.name
        if name not in hmap:
            # new skill - place under software-development
            dst = HERMES_ROOT / "software-development" / name
        else:
            dst = hmap[name]
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(skill_dir, dst)
        print(f"synced {name} -> {dst}")


if __name__ == "__main__":
    main()
