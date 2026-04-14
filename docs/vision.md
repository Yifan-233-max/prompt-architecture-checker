# Vision

## Positioning

Prompt Architecture Checker is an architecture and workflow quality tool for prompt-as-code repositories.

It treats prompt files as executable design artifacts rather than passive documentation.

## Core Thesis

Complex agent systems need the equivalent of:

- type checking for handoffs
- linting for prompt structure
- architecture validation for workflow graphs
- safety checks for resource and tool usage
- regression tests for orchestration behavior

## Design Principles

1. Thin syntax, strong validation.
2. Preserve natural language where possible.
3. Prefer explicit contracts at agent boundaries.
4. Separate deterministic lint from judgment-based review.
5. Validate workflow correctness before stylistic quality.

## Proposed Object Model

### Repository
A repository contains instructions, agents, skills, prompts, memory definitions, artifacts, and routing rules.

### Contract
A contract is a machine-readable layer attached to a prompt artifact. It describes expected inputs, outputs, state reads and writes, allowed tools, and completion criteria.

### Flow Edge
A flow edge represents one explicit handoff or dependency between two prompt artifacts.

### Finding
A finding is a typed result with severity, rationale, location, and recommended fix.

## Checker Modes

### Lint
Deterministic checks for missing files, broken references, route conflicts, undeclared writes, missing cleanup, and contract inconsistencies.

### Review
LLM-assisted review for ambiguity, conflicting goals, hidden assumptions, context budget risk, and weak observability.

### Simulate
Flow analysis to validate resource acquisition and release symmetry, step reachability, and evidence generation expectations.

## Output Targets

- human-readable markdown report
- JSON for downstream tooling
- SARIF for CI and PR annotation

## Likely First Users

- teams building Copilot / agent workflows in repositories
- prompt engineering teams with orchestrator-agent-skill patterns
- maintainers of multi-file instruction systems with persistent memory and artifacts

## Key Success Metric

A maintainer should be able to point the checker at a prompt repository and get a prioritized list of architecture issues before runtime.
