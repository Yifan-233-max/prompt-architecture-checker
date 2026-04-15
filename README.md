# Prompt Architecture Checker

A design-first repository for a prompt-as-code architecture checker.

This project reviews complex prompt-driven, multi-agent systems in the same way linters, static analyzers, and architecture review tools validate codebases. It also includes a prompt architecture reviewer skill and fixture repositories for repository-level review of prompt-as-code systems.

## Problem

Prompt-driven systems accumulate execution logic without a stable syntax layer. That flexibility is useful, but it also creates failure modes that are hard to detect early:

- conflicting instructions across orchestrators, agents, and skills
- missing handoff contracts between agents
- resource acquisition without guaranteed release
- broken file, memory, or artifact references
- prompt steps that exceed context budgets
- ambiguous completion criteria and unverifiable outcomes

## Goal

Build a checker that can:

1. Parse a prompt-as-code repository into an architecture graph.
2. Run deterministic lint rules on prompts, skills, agents, and workflow files.
3. Use LLM-assisted review to detect ambiguity, hidden assumptions, and fragile orchestration.
4. Simulate workflow execution paths to validate state transitions and cleanup behavior.

## First Scope

The first version focuses on design and contracts, not runtime execution:

- prompt graph model
- prompt contract schema
- lint rule catalog
- review output format
- repository layout conventions

## Included Reviewer Skill Assets

- `SKILL.md`: public skill entrypoint
- `reviewer-prompt.md`: detailed review procedure
- `output-format.md`: canonical findings model and report shape
- `examples/good-repo/`, `examples/bad-repo/`, `examples/mixed-repo/`: repository review fixtures and expected outputs

## Proposed Components

- `parser`: extracts agents, skills, instructions, routes, resources, and artifacts
- `graph`: builds the workflow and dependency model
- `lint`: runs static rules with severity and file-level findings
- `review`: uses an LLM to surface ambiguity and architectural risks
- `simulate`: walks declared flows and validates resource and state symmetry
- `report`: outputs markdown, SARIF, and machine-readable JSON

## Repository Layout

- `docs/vision.md`: product vision and architecture
- `docs/lint-rules.md`: initial high-value lint rules
- `schemas/prompt-contract.schema.json`: minimal machine-readable contract schema
- `SKILL.md`: public entrypoint for repository-level prompt architecture review
- `reviewer-prompt.md`: detailed contract, flow, and pattern review procedure
- `output-format.md`: canonical findings schema and report templates
- `examples/`: example prompt-as-code structures, contract snippets, and reviewer fixtures

## Suggested Reading Order

1. `README.md` for repository purpose and quick usage
2. `docs/vision.md` for product direction and architecture framing
3. `SKILL.md` for the public skill contract
4. `reviewer-prompt.md` for the detailed review heuristic
5. `output-format.md` for the report shape
6. `examples/` for fixture repositories and expected outputs

## Review Output Contract

Every finding should include:

- severity
- findingClass
- category
- artifactScope
- message
- evidence
- whyItMatters
- suggestedFix

## Non-Goals

- replacing natural-language prompts with a rigid DSL
- enforcing writing style or tone as a primary quality gate
- executing external tools during lint unless explicitly enabled

## Suggested Product Path

1. Build the core contract and graph model.
2. Implement a local CLI.
3. Add CI integration as a GitHub Action.
4. Consider a GitHub App or VS Code extension after rule maturity.
