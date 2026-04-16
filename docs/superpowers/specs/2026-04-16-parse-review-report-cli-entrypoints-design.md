# Parse / Review / Report CLI Entrypoints Design

## Summary

Add three real user-facing CLI entrypoints for the first product slice:

- `prompt-architecture-checker parse <repo>`
- `prompt-architecture-checker review <repo>`
- `prompt-architecture-checker report <repo>`

These commands should invoke the user's existing AI agent environment through a GitHub Copilot CLI skill runner, but the external command experience should stay simpler than the internal architecture. Users should be able to point the CLI at a repository directly, while the implementation still preserves a staged `parse -> review -> report` pipeline behind the scenes.

## Why This Design

The current repository direction already defines the first product slice as `parse`, `review`, and `report`. What is still missing is a concrete command surface that a user can actually run.

The goal of this design is to make the tool feel like a real CLI without collapsing all three stages into one opaque command:

1. users interact with repositories directly
2. the terminal shows explicit stage progress
3. each command returns one primary result
4. internal stage boundaries remain clean enough for testing and future extension
5. the tool reuses the user's existing agent environment instead of asking the checker to manage model credentials

## Product Goal

A maintainer should be able to run one of three commands against a repository and get AI-generated structure understanding, architecture review, or a final report without having to manually manage intermediate artifacts or separately configure model providers for the checker itself.

## Explicit Non-Goals

- forcing users to pass intermediate artifact files between commands
- configuring model providers directly inside the checker CLI
- making JSON or machine-first output the primary first-version experience
- adding deterministic lint or workflow simulation to the first CLI surface
- turning `review` or `report` into broad all-in-one analyzers with no stage boundaries

## User-Facing Command Surface

The first CLI surface should be:

### `prompt-architecture-checker parse <repo>`

Purpose:

- analyze the repository structure
- summarize major units and likely responsibilities
- produce the key relationship graph
- surface evidence and uncertainties

Final terminal payload:

- parse result only

### `prompt-architecture-checker review <repo>`

Purpose:

- review the repository for first-slice architecture issues

Behavior:

- internally runs `parse` first for the current invocation
- then runs `review` against the parse output

Final terminal payload:

- focused findings only

It should not re-dump the full parse narrative as the final output.

### `prompt-architecture-checker report <repo>`

Purpose:

- produce the final user-ready markdown report

Behavior:

- internally runs `parse`
- internally runs `review`
- then renders the final report

Final terminal payload:

- final markdown report only

## Execution Model

The user experience should be repository-direct, but the implementation should remain stage-driven.

### External model

Users run:

1. `prompt-architecture-checker parse <repo>`
2. `prompt-architecture-checker review <repo>`
3. `prompt-architecture-checker report <repo>`

Users should not need to understand or manage intermediate artifacts by default.

### Internal model

Internally, every invocation still follows stage boundaries:

1. `parse`
2. `review`
3. `report`

Command-specific behavior:

- `parse` invokes `parse-skill` only
- `review` invokes `parse-skill` first if needed, then invokes `review-skill`
- `report` invokes `parse-skill`, then `review-skill`, then `report-skill`

The CLI is responsible for that orchestration. The individual skills should stay focused on their own stage rather than recursively calling one another.

This preserves a clean internal pipeline while keeping the outer command model simple.

## Terminal Experience

The CLI should be terminal-first.

### Default behavior

- print results directly to the terminal
- show explicit stage progress for every stage that runs
- show a short stage summary after each completed stage

Examples:

- `Parsing...`
- `Reviewing...`
- `Reporting...`

### File output

`--out <path>` should write the primary output of the invoked command:

- `parse --out` writes the parse result
- `review --out` writes the review findings
- `report --out` writes the final report

Intermediate stage artifacts should stay internal by default.

First version should not require users to think about internal artifact files unless they explicitly request output.

## Internal Components

The CLI should be implemented with the following internal units.

### 1. CLI command layer

Responsibilities:

- parse command name and arguments
- validate repo path
- parse flags such as `--out`

### 2. Run coordinator

Responsibilities:

- decide which stages must run for the current command
- execute those stages in order
- print stage progress and short stage summaries
- hold the current invocation context in memory

### 3. GitHub Copilot CLI runner adapter

Responsibilities:

- invoke the current GitHub Copilot CLI skill runner
- pass stage-specific context such as repo path and stage goal
- normalize runner responses into checker-owned stage results

### 4. Parse skill invoker

Responsibilities:

- invoke `parse-skill`
- collect:
  - structure summary
  - key relationship graph
  - evidence
  - uncertainties

### 5. Review skill invoker

Responsibilities:

- invoke `review-skill` with parse output
- require it to stay within the approved first-slice categories:
  - handoff and completion problems
  - graph problems
  - implicit state problems

### 6. Report skill invoker

Responsibilities:

- invoke `report-skill` with parse and review outputs
- render the final markdown report returned by that stage
- avoid inventing new conclusions beyond what parse and review already established

### 7. Stage result normalizer

Responsibilities:

- turn runner responses into checker-owned parse, review, and report artifacts
- keep the CLI's stage contracts stable even if runner output evolves

## Data Boundaries

Even though users do not pass artifacts manually by default, the internal data model should still be explicit.

### Parse artifact

Should contain at least:

- repository structure summary
- relationship graph
- evidence for major structural claims
- uncertainties for inferred structure

### Review artifact

Should contain:

- structured findings derived from parse output
- finding metadata aligned with the existing report contract

### Report input

Should consume:

- parse artifact
- review artifact

### Report output

Should produce:

- final markdown report

## Configuration Model

The first CLI version should integrate with the user's existing GitHub Copilot CLI environment rather than asking the checker to manage model selection directly.

### Configuration precedence

1. CLI flags
2. environment variables
3. config file
4. defaults

### First-slice command flags

At minimum:

- `--out`

Runner discovery and any Copilot-specific environment requirements should remain outside the user-facing command contract.

## Failure Boundaries

The first CLI version should fail clearly and by stage.

### Pre-AI failures

Fail before any AI call when:

- the repository path is missing
- the repository path is unreadable
- the repository path is not a supported local repository target

### Runner setup failures

Fail with a setup error when:

- the GitHub Copilot CLI runner is not available
- the required skill cannot be found
- the runner invocation contract is incomplete or invalid

### Stage failures

- if `parse` fails, `review` and `report` must stop immediately
- if `review` fails, `report` must stop immediately
- report should never continue on partial or guessed upstream data

### Stage boundaries

- `review` must not silently reconstruct the repository instead of using parse output
- `report` must not invent findings or conclusions that parse and review did not establish
- skills should not self-orchestrate prerequisite stages that the CLI is already responsible for sequencing

## Testing Strategy

The CLI design should be tested at both command and stage levels.

### Parse tests

Use fixture repositories to verify that `parse` can produce:

- recognizable structure summaries
- usable call and handoff graphs
- explicit evidence and uncertainty markers

### Review tests

Use bad and mixed fixtures to verify that `review` reliably finds:

- handoff and completion issues
- graph issues
- implicit state issues

### Report tests

Use golden outputs to verify that `report` produces a stable markdown structure with:

1. repository structure summary
2. key relationship graph
3. highest-priority findings
4. suggested fixes

### Command tests

Verify:

- `parse <repo>` invokes only `parse-skill`
- `review <repo>` invokes `parse-skill` then `review-skill`
- `report <repo>` invokes `parse-skill` then `review-skill` then `report-skill`
- stage progress is visible in the terminal
- `--out` writes the primary output for the invoked command

## Design Rationale

This design intentionally keeps the user-facing CLI simple while protecting the internal architectural boundaries already approved for the first product slice.

That tradeoff matters:

- a repository-direct command surface makes the tool feel easy to use
- CLI orchestration keeps the implementation testable
- reusing the user's existing Copilot environment avoids turning the checker into a model-configuration product
- terminal-first behavior makes the first version immediately usable without introducing a full artifact management workflow

The result is a CLI that feels like a product entrypoint rather than a developer-only pipeline, while still preserving the `parse -> review -> report` architecture as the core design truth and using three explicit skills as the execution units behind that flow.
