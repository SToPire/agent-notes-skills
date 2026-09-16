# Installation and validation

## Payload

The installer copies `assets/repository/` into the requested root and installs the sibling `agent-notes-write`, `agent-notes-maintain`, and `agent-notes-review` directories under `.agents/skills/`. Keep those siblings beside this startup skill when moving the suite. The startup skill itself remains in the reusable suite.

The project receives `.agents/notes/README.md`, `.agents/notes/AGENTS.md`, `implemented/AGENTS.md`, `archived/AGENTS.md`, an empty archive manifest, and `scripts/agent_notes.py`. A Notes-local `.gitattributes` preserves LF bytes at checkout so Git's automatic CRLF conversion cannot invalidate archive hashes. All four lifecycle directories contain the six class directories. Empty `.gitkeep` files preserve those directories in Git; the checker excludes them from decision records and archive seals.

The installer appends a marked Agent Notes section to root `AGENTS.md`, preserving preceding instructions. It preflights every destination: identical files are retained; different content, non-file destinations, and symlinks at affected paths fail before mutation. An interrupted install can be rerun when previously written files still match the payload. Customized installations require deliberate local maintenance; this command is not an updater.

## Prerequisites

Python 3.10+ runs installation and validation using the standard library. Git is required for archive-baseline checks. An empty archive can be checked before the first Git commit; create the project's initial commit before sealing any historical records.

The installer accepts an existing directory and does not initialize Git, stage files, commit, push, or modify global skill settings. Use `--dry-run` to list the proposed writes. Keep the target outside the suite itself.

## Executed checks

From the installed repository root:

```sh
python3 scripts/agent_notes.py check
```

This command checks directory classification, dated filenames, lifecycle headers, required sections, line endings, and the append-only archive manifest. It does not establish decision quality, correspondence with code, or link validity. The operating skills own those semantic checks and link repair.

`seal` runs the full checker and appends only previously unsealed archive hashes; it refuses changed or missing sealed content.

## CI baseline

Add the read-only `check` command to the project's normal check script. In CI, pass a trusted pre-change commit:

```sh
python3 scripts/agent_notes.py check --base-ref "$AGENT_NOTES_BASE_REF"
```

The CI system must set `AGENT_NOTES_BASE_REF` from its event metadata: the PR's base commit or the push event's before commit. Fetch that commit when checkout history is shallow. Never take the baseline from a file edited by the change under review. An unavailable or invalid explicit ref fails validation. For the first push with no prior commit, the initial empty archive has no prior seals; run the ordinary check.

Local commands compare with committed HEAD by default. CI must use a pre-change commit because comparing a committed change only against itself cannot detect a simultaneous rewrite of an artifact and its seal. Do not run `seal` in CI to repair failing inputs.

If the project has no executed check entrypoint or CI, leave the runnable command in root AGENTS.md and explicitly report that automation is not yet connected. Adding a provider-specific CI system requires a concrete project choice.
