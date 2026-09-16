# Portable Agent Notes Skills

## Summary

Install DSH's Agent Notes mechanism in a fresh repository, then record, review, and maintain engineering decisions with four reusable skills. The suite carries its own rules and checker. It preserves six decision classes, supersession audits, and immutable archives without requiring the DSH workspace or package manager. Each note is one Markdown file, and the supplied documentation and templates are in English.

## Contents

- [Use the suite](#use-the-suite)
- [Skills](#skills)
- [Note scope](#note-scope)
- [Installed files](#installed-files)
- [Extraction from DSH](#extraction-from-dsh)
- [Checks](#checks)
- [Acknowledgements](#acknowledgements)

## Use the suite

Keep this whole directory together. Ask your coding agent to read [agent-notes-startup/SKILL.md](skills/agent-notes-startup/SKILL.md) and install Agent Notes into the absolute path of a new project. Python 3.10+ and Git are the only tool prerequisites; the target must be an existing directory.

For example: “Use the startup skill at `/path/to/agent-notes-skills/skills/agent-notes-startup/SKILL.md` to set up Agent Notes in `/path/to/my-project`.” The startup skill installs the three operating skills into that project and checks the result.

For direct installation, run from this suite's directory, replacing the target path:

```sh
python3 skills/agent-notes-startup/scripts/install.py --target /path/to/my-project --dry-run
python3 skills/agent-notes-startup/scripts/install.py --target /path/to/my-project
```

Then run `python3 scripts/agent_notes.py check` from the target project. The installer preserves existing root instructions and refuses conflicting files before writes. An identical rerun is a no-op; it does not upgrade customized installations. Read the [installation reference](skills/agent-notes-startup/references/installation.md) for CI integration and the trusted archive baseline.

## Skills

| Skill | Operation | Typical request |
|---|---|---|
| [agent-notes-startup](skills/agent-notes-startup/SKILL.md) | Install the Notes structure, rules, checker, and three operating skills. | “Set up Agent Notes in this new repository.” |
| [agent-notes-write](skills/agent-notes-write/SKILL.md) | Write proposals and implemented decisions; update factual realization and rewrite completed proposals. | “Record why this change uses an append-only log.” |
| [agent-notes-maintain](skills/agent-notes-maintain/SKILL.md) | Audit supersession, preserve partial replacements, consolidate, reject, archive, and prune records. | “Reconcile the old decisions affected by this removal.” |
| [agent-notes-review](skills/agent-notes-review/SKILL.md) | Compare records with implementation, evidence, and lifecycle rules. | “Check whether these notes accurately describe the change.” |

The installed project README owns the rules. Skills contain the procedures and decision criteria used to apply them. Writing a new record includes a scoped maintenance audit; a standalone review reports findings unless fixes are also requested.

## Note scope

Notes record project decisions, their reasons, trade-offs, and durable obligations. A proposal states an approach and observable outcomes. Keep local inspection history and incidental implementation plans out of both proposed and implemented records. The writing skill includes [content-selection examples](skills/agent-notes-write/references/decision-scope.md); review checks this scope alongside factual accuracy. Project-adopted versions and exact technical guarantees remain appropriate when the decision depends on them.

## Installed files

```text
project/
  AGENTS.md                         appended Agent Notes entry
  scripts/agent_notes.py            standalone Python checker
  .agents/
    skills/
      agent-notes-write/
      agent-notes-maintain/
      agent-notes-review/
    notes/
      .gitattributes                preserve LF bytes at checkout
      README.md
      AGENTS.md
      proposed/<class>/
      implemented/AGENTS.md
      implemented/<class>/
      rejected/<class>/
      archived/AGENTS.md
      archived/manifest.json
      archived/<class>/
```

Each lifecycle contains `architecture`, `process`, `feature`, `bug-fix`, `simplification`, and `testing`. Empty `.gitkeep` files preserve the directories in Git. Note templates live in the writing skill. The startup installer creates no example decisions, Git commits, global configuration, or provider-specific CI workflow.

## Extraction from DSH

| DSH source | Destination in this suite |
|---|---|
| `.agents/notes/README.md` | Installed project rules: layout, classification, lifecycle, required format, supersession, consolidation, and archive semantics. |
| `.agents/notes/AGENTS.md`, `implemented/AGENTS.md`, `archived/AGENTS.md` | Corresponding installed subtree instructions. |
| `dsh-find-simplifications` | The writing skill's evidence-based proposal authoring; DSH-specific code-search heuristics are excluded. |
| `dsh-prose-standard` and `dsh-trim-cot-leakage` | Writing and review criteria that preserve factual obligations and remove session-only narration. |
| `dsh-archive-agent-notes` | Maintenance skill, including future-value retention and full versus partial supersession. |
| `dsh-code-review` | Decision/implementation agreement and actual verification evidence. |
| Agent Note tree/format/archive scripts | Independent `scripts/agent_notes.py` with `check` and `seal` commands. |
| Root `.gitattributes` LF policy | A Notes-local `.gitattributes` keeps checked-out bytes consistent with their hashes. |

The Python checker adapts DSH's structural rules and SHA-256 archive manifest schema to individual Markdown records. Calendar dates are checked for validity. Blank class placeholders make the fresh tree survive a Git clone. DSH's pre-format exception and retired-path restrictions are omitted because the target has no old decision-record system. DSH-specific links, commands, and historical examples are replaced with self-contained instructions.

Valid links, correct rationale, and agreement with code remain review duties. CI integration uses the project's real check entrypoint and a trusted pre-change Git commit; installation alone does not enforce CI. Current-project rules can evolve locally without reinstalling the starter.

## Checks

From the installed project root, validate the Notes tree:

```sh
python3 scripts/agent_notes.py check
```

After an authorized archive move, run `python3 scripts/agent_notes.py seal` to append hashes for the newly archived notes. Existing seals remain unchanged. Use a trusted pre-change commit for CI checks as described in the installation reference.

The four SKILL.md files also support the `skill-creator` quick validator.

## Acknowledgements

Thanks to the [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) maintainers for the Agent Notes mechanism. This suite adapts its note organization, lifecycle rules, writing and review workflows, and archive checks for reuse in new repositories. The source mapping above identifies the DSH materials used.
