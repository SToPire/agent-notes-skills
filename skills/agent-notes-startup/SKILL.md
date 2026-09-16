---
name: agent-notes-startup
description: Install the DSH-derived Agent Notes directory, rules, templates, maintenance skills, and validation script in a repository that has no decision-record mechanism. Use when the user asks to set up Agent Notes in a new project.
---

# Start Agent Notes

Install a self-contained decision-record system in the target repository. The supplied rules preserve the DSH lifecycle, six classes, supersession audit, and frozen archive. Each note is one Markdown file. Read [the installation reference](references/installation.md) for file destinations, retry behavior, and CI integration.

## Install

1. Establish the target repository from the user's request. Inspect its root instructions and check that it has no existing Agent Notes mechanism. Keep all four skill folders together; the installer copies the three operating skills from this suite.
2. Run the installer with Python 3.10+ and an explicit target path. Resolve the script path relative to this SKILL.md; do not assume the skill lives inside the target repository.

   ```sh
   python3 /path/to/agent-notes-startup/scripts/install.py --target /path/to/project --dry-run
   python3 /path/to/agent-notes-startup/scripts/install.py --target /path/to/project
   ```

3. Read the installed `.agents/notes/README.md`. Verify the appended root AGENTS.md entry, the three installed skills, and the independent checker. If the project has a root instruction alias, confirm it reaches the updated AGENTS.md.
4. From the target root, run `python3 scripts/agent_notes.py check`. Wire that command into the project's executed check entrypoint and CI when one exists. For CI archive protection, supply its trusted pre-change commit as described in the installation reference. Do not claim CI enforcement from a written instruction alone.
5. Report the installed paths, the checks actually run, and whether CI is connected. A first engineering decision can be recorded with `agent-notes-write` when the user's task includes one.

Installing into the requested repository is part of this task. The installer creates no commits and contacts no external services. Conflicting files are reported before writes; diagnose the named file instead of overwriting it. An identical rerun leaves existing bytes unchanged.

## Result

The project owns its installed rules and operating skills. Read those local rules for subsequent work. The starter templates contain no decisions from the source project. Existing ADR migrations and rule-evolution programs are outside this skill's scope.
