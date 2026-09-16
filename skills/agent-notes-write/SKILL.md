---
name: agent-notes-write
description: Create or update Agent Notes for substantial proposals and implemented engineering decisions in a repository using the Agent Notes mechanism. Use when a change needs recorded rationale, alternatives, consequences, or a proposal-to-implementation rewrite.
---

# Write Agent Notes

Record the reasons and trade-offs that future maintainers need. This workflow assumes the project has the Notes mechanism installed. Read `.agents/notes/README.md` and the applicable AGENTS.md files from the target repository; those files own the rules. If absent, use the startup skill from the complete suite before writing.

## Establish the decision

1. Read the requested change, current implementation, relevant tests, and existing active notes. Search by mechanism, symbols, and rejected alternatives. Follow an archived citation only when needed as historical evidence; do not use it as current authority.
2. Decide whether this change needs a note under the project's non-trivial-change rule. An existing owner can be updated when the decision remains the same. A reversal needs a new note and explicit links to the prior decision.
3. Choose the lifecycle and one class using the project README. Substantial future or partly implemented work is proposed. A completed decision starts directly in implemented; completing a proposal moves and rewrites it. Preserve the first-proposed date.

## Write and reconcile

Use the matching template in [assets/](assets/) for a new proposal or implemented record. Replace all template fields. Each note is one Markdown file. A rejected record retains its proposal body; only its status verdict changes.

State the problem independently of the chosen solution. Record actual alternatives and why they lost; distinguish documented deliberation from a comparison performed during this task. If historical reasons cannot be established, report the evidence gap rather than inventing them. New proposals can explicitly compare keeping the current behavior with the proposed change.

Describe implemented behavior in the present tense. Preserve benefits, costs, required verification, and named coverage gaps. Cite repository files present in the current change, durable project records, or external standards. Keep content understandable without the authoring conversation: remove session-only citations, reviewer dialogue, task codes, and test walkthroughs while retaining every meaningful condition, obligation, exception, and consequence.

Every new note includes a scoped supersession audit using the installed `agent-notes-maintain` workflow. Search the same mechanism and process affected by the decision. Resolve known full or partial overlaps in this change; do not defer them to a future cleanup. A proposal-to-implementation move includes the body rewrite and inbound-link repair.

## Verify and report

Review the note's claims, headings, code, and links. Keep one physical line per paragraph and exactly one trailing newline. Then run from the repository root:

```sh
python3 scripts/agent_notes.py check
```

Run relevant project checks when verifying implementation claims, and report only evidence actually observed. Review links from and into active notes. Report the owning note, its status, any superseded records and their disposition, and remaining factual gaps. Writing a note does not authorize committing or publishing it.
