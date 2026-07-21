#!/usr/bin/env python3
"""Strictly verify Agent Skills structure and ModernUO package consistency."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK = re.compile(r"\[[^]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
MOJIBAKE = ("â€”", "â€“", "â†’", "Ã", "�")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="fail on package documentation and catalog drift")
    args = parser.parse_args()
    skills_root = root / "plugins" / "modernuo" / "skills"
    errors: list[str] = []
    skills = sorted(p for p in skills_root.iterdir() if (p / "SKILL.md").is_file())
    for skill in skills:
        try:
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            parts = text.split("---", 2)
            if len(parts) != 3 or parts[0].strip():
                fail(errors, f"{skill.name}: invalid frontmatter")
                continue
            data = yaml.safe_load(parts[1])
            manifest = json.loads((skill / "manifest.json").read_text(encoding="utf-8"))
            interface = yaml.safe_load((skill / "agents" / "interface.yaml").read_text(encoding="utf-8"))
            name = data.get("name")
            version = str((data.get("metadata") or {}).get("version", ""))
            if name != skill.name or not NAME.fullmatch(str(name)):
                fail(errors, f"{skill.name}: invalid or mismatched name")
            if not data.get("description"):
                fail(errors, f"{skill.name}: missing description")
            if manifest.get("name") != name or manifest.get("version") != version or not version:
                fail(errors, f"{skill.name}: manifest identity mismatch")
            if not interface.get("interface", {}).get("default_prompt"):
                fail(errors, f"{skill.name}: missing default prompt")
            for rel in ("evals/baseline_description.txt", "evals/trigger_cases.json", "evals/semantic_config.json"):
                path = skill / rel
                if not path.is_file():
                    fail(errors, f"{skill.name}: missing {rel}")
                elif path.suffix == ".json":
                    json.loads(path.read_text(encoding="utf-8"))
            for path in skill.rglob("*"):
                if not path.is_file():
                    continue
                content = path.read_text(encoding="utf-8")
                if any(marker in content for marker in MOJIBAKE):
                    fail(errors, f"{path.relative_to(root)}: mojibake")
                if path.suffix == ".md":
                    for target in LINK.findall(content):
                        clean = target.split("#", 1)[0]
                        if clean and not (path.parent / clean).resolve().exists():
                            fail(errors, f"{path.relative_to(root)}: broken link {target}")
        except (OSError, ValueError, TypeError, json.JSONDecodeError, yaml.YAMLError) as exc:
            fail(errors, f"{skill.name}: {exc}")
    versions = []
    for rel in ("plugins/modernuo/.codex-plugin/plugin.json", "plugins/modernuo/.claude-plugin/plugin.json", "plugins/modernuo/.cursor-plugin/plugin.json"):
        versions.append(json.loads((root / rel).read_text(encoding="utf-8"))["version"])
    if len(set(versions)) != 1:
        fail(errors, "ModernUO plugin manifest versions differ")
    if args.strict:
        readme = (root / "README.md").read_text(encoding="utf-8")
        catalog = (skills_root / "SKILL-CATALOG.md").read_text(encoding="utf-8")
        if f"packages {len(skills)} English Agent Skills" not in readme:
            fail(errors, "README skill count is stale")
        if f"Current ModernUO plugin inventory: {len(skills)} skills." not in catalog:
            fail(errors, "catalog skill count is stale")
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({"skill_count": len(skills), "passing": len(skills), "failing": 0, "plugin_version": versions[0]}))


if __name__ == "__main__":
    main()
