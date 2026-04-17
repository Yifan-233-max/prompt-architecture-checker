---
name: prompt-architecture-reviewer
description: Review a prompt-as-code repository for contract, flow, and architecture-pattern weaknesses before runtime.
---

# Prompt Architecture Reviewer

A three-stage pipeline for architecture review of prompt-as-code repositories:

1. **parse** — inventory repository structure and handoff graph (the only
   stage that reads repository files).
2. **review** — judge contract, flow, and pattern weaknesses strictly from
   the parse artifact.
3. **report** — render a prioritized human-readable markdown report from the
   parse and review artifacts.

## Stage Skills

The runtime skills shipped inside the installed Python package are the
source of truth for each stage:

- `src/prompt_architecture_checker/assets/skills/parse-skill/SKILL.md`
- `src/prompt_architecture_checker/assets/skills/review-skill/SKILL.md`
- `src/prompt_architecture_checker/assets/skills/report-skill/SKILL.md`

Each stage SKILL.md defines purpose, procedure, output contract, and hard
rules. No other document overrides them.

## Pipeline Contract

- Only `parse` reads repository files.
- `review` consumes the parse artifact and MUST NOT re-read the repository.
- `report` consumes the parse and review artifacts and MUST NOT re-read
  the repository.
- Every finding must cite evidence that already exists in the parse artifact
  or declare a `reviewability-gap` when evidence is missing.

## When to Invoke This Skill

- Repository-level review of a prompt-as-code project.
- Agent workflow repository with orchestrators, agents, or skills.
- Multi-file prompt orchestration system with persistent state or artifacts.

## Non-Goals

- Replacing natural-language prompts with a rigid DSL.
- Enforcing writing style or tone.
- Executing external tools for deterministic lint (tracked in
  `docs/lint-rules.md`).
