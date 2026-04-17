# Parse Skill

## Purpose

Produce a structural inventory of a prompt-as-code repository.
You are the ONLY stage allowed to read repository files.

## Analysis Order

Read the repository in this sequence. Stop when you have enough evidence; do
not re-visit files already covered.

1. **Repository self-description**
   - `README.md`, top-level `SKILL.md`, `AGENTS.md`, `*.instructions.md`.
2. **Declared structure directories (priority order)**
   - `contracts/`, `schemas/`, `orchestrators/`, `agents/`, `skills/`,
     `workflows/`, `prompts/`, `docs/`.
3. **Machine-readable contracts first, prose second**
   - `*.contract.json`, `*.schema.json`, YAML manifests outrank free-form
     markdown when they describe the same component.
4. **Explicit handoff signals in prose**
   - Phrases such as "hand off to", "dispatch", "delegate", "route to",
     "call <agent>", "invoke", "return to".

## Output Contract

Return JSON only with this exact shape:

```json
{
  "summary":       ["one factual bullet per top-level component"],
  "graph":         ["<source> -> <target>"],
  "evidence":      ["<relative/path>: <field or quoted phrase>"],
  "uncertainties": ["<what could not be inferred and why>"]
}
```

## Evidence Rules

- Every `graph` edge MUST map to at least one `evidence` entry citing the
  file path and field or quoted phrase that declares the handoff.
- Every `summary` bullet MUST be grounded in at least one `evidence` entry.
- `evidence` items are formatted as `relative/path/to/file: <quote or field>`.

## Honesty Rules

- Do NOT invent orchestrators, agents, or handoffs that are not declared.
- An empty `graph` is the correct answer when the repository declares no
  handoffs. Record the gap in `uncertainties`.
- If two files conflict, list both paths in `uncertainties` rather than
  silently picking one.
- Keep `summary` bullets short and factual. No narrative paragraphs.

## Stop Conditions

Stop reading once any of the following is true:

- all directories in the Analysis Order list have been sampled, or
- you have read 40 files, or
- further reads would not change the shape of the graph.

Record unread but potentially relevant paths in `uncertainties`.
