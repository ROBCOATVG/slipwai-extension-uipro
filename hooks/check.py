#!/usr/bin/env python3
"""Fail when the skill this extension installs is adopted and not here, or is not the pinned one.

`skills/ui-ux-pro-max/` is ignored by Git — it is installed by `./init --extension uipro` from a pinned CLI
— so a fresh clone and every CI runner has the election and not the skill. **State that can go stale and
that nothing checks is state nobody trusts and everybody rebuilds**, which is the obligation this file
answers (`docs/extensions.md`, obligation 5).

Three states, and each is said rather than guessed at:

* **Not adopted.** No `.slipwai/extensions.json` naming `uipro`, or no browser app to design for: nothing
  to check, and `make verify` is not the place to argue about an optional tool.
* **Adopted, not installed here.** Reported as *skipped* by default, because a clone that has not run
  `./init` is the ordinary case and not a fault — and as a *failure* where `UIPRO_REQUIRE=1`, which is what
  to set wherever the skill is expected to be present.
* **Adopted and installed.** The skill's own `SKILL.md` must be there and must carry the capability line
  `./init` writes into it; a directory with no `SKILL.md` is a half-finished install, which is exactly the
  stale state this exists to catch.

Never fatal on its own terms beyond that: `scripts/extensions/hooks.py check --fatal` is what makes a
`check` hook a gate, and `make verify` is the only caller that passes it.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
SKILL = "ui-ux-pro-max"
KEY = "uipro"


def project_root(script: Path) -> Path:
    for candidate in script.parents:
        if (candidate / "project.json").is_file():
            return candidate
    return script.parents[2]


ROOT = project_root(HERE)
INSTALLED = ROOT / "skills" / SKILL
ELECTED = ROOT / ".slipwai/extensions.json"


def adopted() -> bool:
    """Whether this project elected `uipro`. Absent or unreadable is *not adopted*: a project that never
    asked for an optional tool is not a project with a problem."""
    try:
        held = json.loads(ELECTED.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeDecodeError):
        return False
    named = held.get("extensions") if isinstance(held, dict) else held
    return KEY in named if isinstance(named, list | dict) else False


def browser_apps() -> list[str]:
    """The deployables that declare a `frontend` capability and are still here. None is nothing to design
    for, which is the same answer `init.py` gives."""
    try:
        deployables = json.loads((ROOT / "project.json").read_text(encoding="utf-8")).get("deployables")
    except (OSError, ValueError, UnicodeDecodeError):
        return []
    if not isinstance(deployables, dict):
        return []
    return [str(one.get("path")) for one in deployables.values()
            if isinstance(one, dict) and "frontend" in (one.get("capabilities") or [])
            and (ROOT / str(one.get("path", ""))).is_dir()]


def main() -> int:
    if not adopted():
        print("check-uipro: not adopted here; nothing to check")
        return 0
    if not browser_apps():
        print("check-uipro: adopted, and this project has no browser app to design for; nothing to check")
        return 0
    if not INSTALLED.is_dir():
        required = os.environ.get("UIPRO_REQUIRE") == "1"
        said = (f"check-uipro: skills/{SKILL}/ is not here. It is ignored by Git, so a fresh clone and a CI "
                f"runner have the election and not the skill.\n"
                f"Install it:\n"
                f"  ./init --extension uipro")
        print(said, file=sys.stderr if required else sys.stdout)
        return 1 if required else 0
    skill_md = INSTALLED / "SKILL.md"
    if not skill_md.is_file():
        print(f"check-uipro: skills/{SKILL}/ is here and has no SKILL.md, so the install did not finish.\n"
              f"Install it again:\n"
              f"  ./init --extension uipro", file=sys.stderr)
        return 1
    if "capability" not in skill_md.read_text(encoding="utf-8"):
        print(f"check-uipro: skills/{SKILL}/SKILL.md carries no capability line, so it is not the copy "
              f"`./init` wrote — a hand-replaced or part-installed skill.\n"
              f"Install it again:\n"
              f"  ./init --extension uipro", file=sys.stderr)
        return 1
    print(f"check-uipro: skills/{SKILL}/ is installed and complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
