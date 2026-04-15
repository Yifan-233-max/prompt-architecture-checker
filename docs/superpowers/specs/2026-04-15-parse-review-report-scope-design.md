# Parse / Review / Report First-Scope Design

## Summary

Refocus the first version of Prompt Architecture Checker around three core capabilities only:

- `parse`
- `review`
- `report`

The first version should not present `lint`, `simulate`, or a separate `graph` subsystem as primary product components. Instead, `graph` becomes a structured output of `parse`, and contract/schema ideas remain lightweight supporting concepts rather than top-level product pillars.

## Why Change The Scope

The current README describes a broader checker vision that includes deterministic lint and workflow simulation. That long-term direction is still valid, but it is too wide for the first meaningful product slice.

The most valuable first capability is narrower:

1. Use AI to understand how a prompt-as-code repository is structured.
2. Surface the repository's call flow and handoff relationships.
3. Review that structure for the highest-value architecture problems.
4. Present the result as a readable report.

This reduces the first version to the shortest path that still proves the product thesis.

## Product Goal For The First Version

A maintainer should be able to point the tool at a prompt-as-code repository and get:

1. an AI-generated structural summary of the system
2. a key relationship graph showing who calls whom and how handoffs flow
3. a focused review of the most important architecture problems
4. a final report that combines structure and findings in one place

## Explicit Non-Goals For The First Version

- deterministic lint as a first-class product mode
- full workflow simulation
- broad tool-policy or side-effect analysis
- deep contract authoring workflows
- large numbers of rule categories
- machine-first output formats as the primary user experience

## Proposed Components

### 1. `parse`

`parse` is the core first-version capability.

It is not a traditional syntax parser. It is an AI repository interpreter that reads the important files in a prompt-as-code project and produces two outputs:

1. **Structure summary**
   - what orchestrators, agents, skills, prompts, or workflows exist
   - what each major unit appears to do
   - where the likely entrypoints and control hubs are

2. **Relationship graph**
   - who calls whom
   - where handoffs appear to happen
   - which nodes look like fan-in or fan-out hubs
   - where implicit dependencies are likely present

`parse` should also emit:

- **evidence** for every major structural claim
- **uncertainties** where the interpretation depends on inference rather than explicit declaration

For first-version scope, `graph` is not a separate component. It is the structured output of `parse`.

### 2. `review`

`review` consumes the output of `parse` rather than re-explaining the repository from scratch.

Its first-version scope is intentionally narrow. It should focus on only three categories:

1. **handoff and completion problems**
   - missing expected outputs
   - vague handoffs
   - unclear completion signals

2. **graph problems**
   - cycles without clear bounds
   - unreachable steps
   - outputs that are never consumed

3. **implicit state problems**
   - hidden shared-state dependencies
   - undeclared reads and writes
   - state artifacts whose shape or ownership is unclear

This keeps `review` focused on the user's highest-value architecture concerns instead of turning it into a broad checker too early.

### 3. `report`

`report` is the final delivery layer.

Its job is not only to format findings, but to combine the structural understanding from `parse` with the focused findings from `review`.

The recommended first-version report shape is:

1. **Repository structure summary**
2. **Key relationship graph**
3. **Highest-priority findings**
4. **Suggested fixes**

Markdown should be the primary first-version output. JSON can exist as an internal interchange format, but it should not dominate the public first-version story.

## Command Model

The command surface should reflect the reduced scope directly:

### `parse <repo>`

Outputs:

- human-readable structure summary
- key relationship graph
- evidence and uncertainty annotations

Internal artifact:

- a thin graph-like structure with nodes, edges, evidence, and uncertainties

### `review <parsed-artifact>`

Outputs:

- focused findings in the three first-version categories

Boundary:

- `review` should not redo full repository interpretation

### `report <parse + review>`

Outputs:

- final markdown report combining structure and findings

Boundary:

- `report` should not invent new conclusions; it should organize what `parse` and `review` already established

## Data Flow

The first-version pipeline should be linear:

1. repository input
2. `parse`
3. structured parse artifact
4. `review`
5. findings
6. `report`
7. final markdown output

This linear flow keeps boundaries clear:

- `parse` understands
- `review` judges
- `report` communicates

## Reliability Boundaries

Because the first version is AI-first, it needs explicit guardrails.

### `parse` guardrails

- every important interpretation should include evidence
- uncertain interpretations should be labeled explicitly
- the output should distinguish direct observation from inferred structure

### `review` guardrails

- every finding should point back to parse evidence
- findings should stay within the three first-version categories
- review should prefer concrete structural problems over broad commentary

### `report` guardrails

- no new claims that did not appear in parse or review
- separate system description from issue prioritization
- keep the report readable by maintainers, not only by downstream tools

## Testing Strategy

Testing should stay lightweight and aligned with the reduced scope.

### Parse tests

Use a small set of prompt-as-code example repositories to verify that `parse` can consistently produce:

- a recognizable structure summary
- a usable call/handoff graph
- explicit evidence and uncertainty markers

### Review tests

Use bad and mixed examples to verify that `review` reliably finds:

- handoff and completion issues
- graph issues
- implicit state issues

### Report tests

Use golden markdown outputs to verify that the final report keeps a stable, readable structure.

## README Changes Required

The README should be updated to match this reduced first-version scope.

### Keep

- the overall problem statement
- the long-term product vision

### Change

#### `Goal`

Keep the broad long-term goal, but avoid presenting all future modes as equal first-version priorities.

#### `First Scope`

Rewrite it so the first version is explicitly centered on:

- AI-assisted repository structure understanding
- relationship graph generation
- focused review of high-value architecture problems
- markdown reporting

#### `Proposed Components`

Replace the current list with:

- `parse`: interprets a prompt-as-code repository and produces a structure summary plus relationship graph
- `review`: analyzes parse output for high-value architecture issues
- `report`: produces the final structure-and-findings report

Also note explicitly:

- `graph` is part of `parse`
- `lint` and `simulate` are future directions, not first-version primary components

## Trade-Offs

### Why not keep `graph` separate?

For the first version, separating `graph` from `parse` creates an internal distinction that does not create product value. Users want a structure understanding step; the graph is part of that result.

### Why not start with deterministic lint?

Deterministic lint is valuable, but it is not the shortest path to proving that the tool can understand prompt architecture and reveal the most important workflow problems.

### Why pure AI first?

Because the immediate product question is whether the system can understand prompt orchestration structure well enough to explain it and review it. A heavier hybrid extractor may be a better later architecture, but it is not required to validate the first-version user value.
