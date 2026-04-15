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

1. Use AI to interpret a prompt-as-code repository into a structure summary and relationship graph.
2. Review that structure for high-value architecture issues such as weak handoffs, graph problems, and implicit state dependencies.
3. Produce a final report that combines repository structure, findings, and suggested fixes.
4. Evolve toward deterministic lint and workflow simulation after the first slice proves the core value.

## First Scope

The first version focuses on AI-assisted structure understanding and focused architecture review:

- repository structure summary
- call / handoff relationship graph
- review of handoff, graph, and implicit state issues
- markdown report output
- evidence and uncertainty annotations

## Proposed Components

- `parse`: interprets a prompt-as-code repository and produces a structure summary plus relationship graph
- `review`: analyzes parse output for high-value architecture issues
- `report`: produces the final structure-and-findings report

## Repository Layout

- `docs/vision.md`: product vision and architecture
- `docs/lint-rules.md`: initial high-value lint rules
- `schemas/prompt-contract.schema.json`: minimal machine-readable contract schema
- `examples/`: example prompt-as-code structures, contract snippets, and sample parse / review / report outputs

## Non-Goals

- replacing natural-language prompts with a rigid DSL
- enforcing writing style or tone as a primary quality gate
- executing external tools during lint unless explicitly enabled

## Suggested Product Path

1. Ship the parse / review / report first slice.
2. Add deterministic lint once the parse artifact stabilizes.
3. Add CI integration as a GitHub Action.
4. Consider workflow simulation after graph and review maturity.
