#!/usr/bin/env python3
"""Ad-hoc era-ledger + epic doc consistency (optional dotnet filters).

Env:
  REBIRTHUO_SERVICE — path to service repo
  HERMES_WORKSPACE — workspace with epic/manifest
  ERA_SLUG — ledger filename slug (default mondains-legacy)
  MLQUESTS_CFG_LINES — default 285
  ML_MONSTER_ROWS — default 83
  RUN_DOTNET=1 — run Spellweaving (53) + MLQuest (202) filters

Exit 0 = checks passed; does not prove OSI gameplay parity.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

SERVICE = Path(os.environ.get("REBIRTHUO_SERVICE", r"C:\Users\Jsiem\Documents\GitHub\RebirthUO\service"))
WORKSPACE = Path(os.environ.get("HERMES_WORKSPACE", Path.home() / "workspace"))

ERA_SLUG = os.environ.get("ERA_SLUG", "mondains-legacy")
EXPECTED_CFG_LINES = int(os.environ.get("MLQUESTS_CFG_LINES", "285"))
EXPECTED_MANIFEST_ROWS = int(os.environ.get("ML_MONSTER_ROWS", "83"))
RUN_DOTNET = os.environ.get("RUN_DOTNET", "").strip() in ("1", "true", "yes")

ledger = SERVICE / "dev-docs" / "eras" / f"{ERA_SLUG}.md"
epic = WORKSPACE / f"rebirthuo-epic-ML-PARITY-000-{ERA_SLUG}.md"
manifest = WORKSPACE / "ml-monsters-manifest.tsv"
cfg = SERVICE / "Distribution" / "Data" / "MLQuests.cfg"
proj = SERVICE / "Projects" / "UOContent.Tests" / "UOContent.Tests.csproj"
errors = []


def ok(msg):
    print(f"  OK: {msg}")


def fail(msg):
    errors.append(msg)
    print(f"  FAIL: {msg}")


def dotnet_count(filter_expr, want):
    p = subprocess.run(
        ["dotnet", "test", str(proj), "--filter", filter_expr, "--no-restore", "-v", "q"],
        cwd=SERVICE,
        capture_output=True,
        text=True,
        timeout=300,
    )
    m = re.search(r"erfolgreich:\s*(\d+)", p.stdout + p.stderr)
    got = int(m.group(1)) if m else -1
    if p.returncode != 0 or got != want:
        fail(f"dotnet {filter_expr} -> {got} (want {want})")
    else:
        ok(f"dotnet {filter_expr} -> {want} passed")


def main():
    print("=== hermes-verify-era-ledger-docs (ad-hoc) ===")
    if not ledger.is_file():
        fail(f"ledger missing: {ledger}")
    else:
        t = ledger.read_text(encoding="utf-8")
        if str(EXPECTED_CFG_LINES) not in t:
            fail(f"ledger should mention cfg count {EXPECTED_CFG_LINES}")
        else:
            ok("ledger cfg count reference")
        if "Review-Standard" in t:
            ok("ledger review standard section")
        else:
            fail("ledger missing Review-Standard section")
        if "## Open research" in t:
            fail("ledger uses deprecated Open research section")
        if "| Partial |" in t:
            fail("ledger has forbidden Partial table cell")
        if "| Partial |" not in t:
            ok("ledger no Partial table cells")

    if epic.is_file():
        et = epic.read_text(encoding="utf-8")
        if str(EXPECTED_CFG_LINES) not in et:
            fail(f"epic should mention {EXPECTED_CFG_LINES} cfg bindings")
        else:
            ok("epic cfg count")
    else:
        ok("epic file optional (skip)")

    if manifest.is_file():
        lines = manifest.read_text(encoding="utf-8").strip().splitlines()
        want = EXPECTED_MANIFEST_ROWS + 1
        if len(lines) != want:
            fail(f"manifest lines {len(lines)} != {want}")
        else:
            ok(f"manifest {EXPECTED_MANIFEST_ROWS} rows")
        ml = SERVICE / "Projects" / "UOContent" / "Mobiles" / "Monsters" / "ML"
        stems = {p.stem.replace(" ", "") for p in ml.rglob("*.cs")}
        for ln in lines[1:]:
            name = ln.split("\t")[1]
            if name.replace(" ", "") not in stems:
                fail(f"manifest monster missing .cs: {name}")
                break
        else:
            ok("manifest stems match ML/")
    else:
        ok("manifest optional (skip)")

    if cfg.is_file():
        n = sum(
            1
            for line in cfg.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
        if n != EXPECTED_CFG_LINES:
            fail(f"MLQuests.cfg lines {n} != {EXPECTED_CFG_LINES}")
        else:
            ok(f"MLQuests.cfg = {EXPECTED_CFG_LINES}")
    else:
        fail(f"cfg missing: {cfg}")

    if RUN_DOTNET and proj.is_file():
        dotnet_count("FullyQualifiedName~Spellweaving", 53)
        dotnet_count("FullyQualifiedName~MLQuest", 202)
    elif RUN_DOTNET:
        fail(f"UOContent.Tests csproj missing: {proj}")
    else:
        ok("RUN_DOTNET not set (skip dotnet)")

    if errors:
        print("=== RESULT: FAILED ===")
        return 1
    suffix = " + dotnet filters" if RUN_DOTNET else ""
    print(f"=== RESULT: PASSED (ad-hoc docs{suffix}) ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())