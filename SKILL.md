---
name: prompt-architecture-reviewer
description: Review a prompt-as-code repository for contract, flow, and architecture-pattern weaknesses before runtime.
---

# Prompt Architecture Reviewer

## Outcome

Return a severity-ranked findings list with evidence and concrete modification suggestions.

## Hard Gates

- Review the repository structure before making conclusions.
- Build a structural inventory of orchestrators, agents, skills, workflows, state, artifacts, and handoffs.
- Separate confirmed findings, high-risk signals, and reviewability gaps.
- Do not claim runtime behavior unless the repository evidence supports it.
- Focus on contract, flow, and architecture-pattern issues before style.

## Workflow

1. Inspect the repository tree and main documentation.
2. Identify the core artifacts and likely subsystem boundaries.
3. Follow `reviewer-prompt.md` for the detailed review procedure.
4. Format the final report using `output-format.md`.

## Required Report Shape

Every finding must include:

- severity
- findingClass
- category
- artifactScope
- message
- evidence
- whyItMatters
- suggestedFix

Sort findings by severity first, then by architectural impact.

## Review Focus

- contract gaps
- weak or ambiguous handoffs
- hidden shared-state coupling
- unclear completion signals
- architecture-pattern weaknesses
- reviewability gaps caused by implicit structure
