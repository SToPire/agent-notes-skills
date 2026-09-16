#!/usr/bin/env python3
"""Install the Agent Notes payload and three operating skills without overwrites."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


OPERATING_SKILLS = ("agent-notes-write", "agent-notes-maintain", "agent-notes-review")
CLASSES = ("architecture", "process", "feature", "bug-fix", "simplification", "testing")
START = "<!-- agent-notes:start -->"
END = "<!-- agent-notes:end -->"
ROOT_RULE = f"""{START}
## Agent Notes

Every non-trivial change adds or updates an [Agent Note](.agents/notes/README.md) in the same PR; purely mechanical or local edits without a decision change are exempt. Use [agent-notes-write](.agents/skills/agent-notes-write/SKILL.md) to record proposals and decisions. Every new note includes a scoped supersession check through [agent-notes-maintain](.agents/skills/agent-notes-maintain/SKILL.md).

Keep notes concise and at project-decision scope: rationale, trade-offs, and durable obligations. Local inspection history and incidental implementation plans belong outside the note; follow the [content rules](.agents/notes/README.md#decision-scope).

Keep implemented records current with code in the same change. Review decision/implementation agreement with [agent-notes-review](.agents/skills/agent-notes-review/SKILL.md). Archived notes are frozen historical snapshots, never current authority.

Run `python3 scripts/agent_notes.py check` before submitting changes to the Notes tree. Repair inbound links whenever a note moves or is deleted. CI archive checks use a trusted pre-change commit through `AGENT_NOTES_BASE_REF`.
{END}
"""


def add_tree(source: Path, prefix: Path, payload: dict[Path, bytes]) -> None:
    """Collect regular source files, excluding Python execution residue."""
    for path in sorted(source.rglob("*")):
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError(f"payload contains a symlink: {path}")
        if path.is_file():
            payload[prefix / path.relative_to(source)] = path.read_bytes()


def installation_plan(target: Path) -> dict[Path, bytes]:
    """Preflight all files and return only the required writes."""
    skill = Path(__file__).resolve().parents[1]
    suite_skills = skill.parent
    if not target.is_dir():
        raise ValueError("target must be an existing repository directory")
    suite_root = suite_skills.parent
    if target == suite_root or suite_root in target.parents:
        raise ValueError("target must be outside the reusable skill suite")
    payload = {}
    add_tree(skill / "assets/repository", Path(), payload)
    for name in OPERATING_SKILLS:
        sibling = suite_skills / name
        if not (sibling / "SKILL.md").is_file():
            raise ValueError(f"missing sibling skill {name}; keep the four skill folders together")
        add_tree(sibling, Path(".agents/skills") / name, payload)
    for lifecycle in ("proposed", "implemented", "rejected", "archived"):
        for kind in CLASSES:
            payload[Path(".agents/notes") / lifecycle / kind / ".gitkeep"] = b""
    root_instructions = target / "AGENTS.md"
    if root_instructions.is_symlink() or (root_instructions.exists() and not root_instructions.is_file()):
        raise ValueError("AGENTS.md must be a regular file")
    original = root_instructions.read_bytes() if root_instructions.exists() else b""
    text = original.decode("utf-8")
    if START in text or END in text:
        if text.count(START) != 1 or text.count(END) != 1 or text.index(END) < text.index(START):
            raise ValueError("AGENTS.md has an incomplete or duplicate Agent Notes block")
        block = text[text.index(START):text.index(END) + len(END)]
        if block != ROOT_RULE.rstrip("\n"):
            raise ValueError("AGENTS.md Agent Notes block differs; preserve local rules and review manually")
        payload[Path("AGENTS.md")] = original
    else:
        prefix = original.rstrip(b"\n") + b"\n\n" if original else b"# AGENTS.md\n\n"
        payload[Path("AGENTS.md")] = prefix + ROOT_RULE.encode()
    writes = {}
    for relative, data in payload.items():
        destination = target / relative
        for path in (destination, *destination.parents):
            if path == target:
                break
            if path.is_symlink():
                raise ValueError(f"refusing symlink destination: {path}")
            if path != destination and path.exists() and not path.is_dir():
                raise ValueError(f"destination parent is not a directory: {path}")
        if destination.exists():
            if not destination.is_file():
                raise ValueError(f"destination is not a file: {destination}")
            if destination.read_bytes() == data:
                continue
            if relative != Path("AGENTS.md"):
                raise ValueError(f"conflicting file: {destination}; no files written")
        writes[relative] = data
    return writes


def main() -> int:
    """Install into an explicit target or print the preflighted write plan."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    target = args.target.resolve()
    try:
        writes = installation_plan(target)
        for relative, data in sorted(writes.items()):
            print(relative.as_posix())
            if not args.dry_run:
                destination = target / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                mode = "wb" if relative == Path("AGENTS.md") else "xb"
                with destination.open(mode) as output:
                    output.write(data)
        print(f"{'Would write' if args.dry_run else 'Wrote'} {len(writes)} file(s) in {target}")
        return 0
    except (OSError, ValueError) as error:
        print(f"Agent Notes installation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
