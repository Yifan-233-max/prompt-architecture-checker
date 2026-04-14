# Prompt Architecture Checker

A design-first repository for a prompt-as-code architecture checker.

This project is intended to review complex prompt-driven, multi-agent systems in the same way linters, static analyzers, and architecture review tools validate codebases.

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
- `examples/`: example prompt-as-code structures and contract snippets

## Non-Goals

- replacing natural-language prompts with a rigid DSL
- enforcing writing style or tone as a primary quality gate
- executing external tools during lint unless explicitly enabled

## Suggested Product Path

1. Build the core contract and graph model.
2. Implement a local CLI.
3. Add CI integration as a GitHub Action.
4. Consider a GitHub App or VS Code extension after rule maturity.
