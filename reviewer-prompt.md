# Detailed Reviewer Prompt

## Purpose

Review parse output for contract, flow, and architecture-pattern weaknesses before runtime.

## Review Sequence

1. Read the parse structure summary, relationship graph, evidence, and uncertainties.
2. Use that parse output as the review input rather than rebuilding the full repository inventory from scratch.
3. Separate explicit parse-backed evidence from inferred structure and risk.
4. Review the parse output through the contract, flow, and pattern lenses below.
5. If parse evidence is missing for a claim you need to make, record that as a reviewability gap instead of silently reconstructing the whole repository.
6. Merge overlapping findings and rank them by severity.
7. Produce concrete repair suggestions tied to parse evidence and stated uncertainties.

## Contract Lens

Look for:

- missing declared outputs
- handoffs without expected outputs
- state writes that are implicit instead of declared
- completion criteria that cannot be verified
- referenced files, artifacts, or memory paths that do not close the loop

## Flow Lens

Look for:

- success paths without clear downstream consumption
- failure paths that skip cleanup or evidence capture
- releases or reporting steps that are not reachable from all important paths
- workflow stages that appear ordered only by implication

Only make flow claims that are visible from declared or strongly inferable repository structure.

## Pattern Lens

Look for:

- orchestrators that own too many responsibilities
- hidden coupling through shared memory
- helpers that rely on unstated context
- architecture layers that collapse planning, execution, and reporting into one unit
- cycles between collaborators without explicit bounds

## Findings Classes

### Confirmed Findings

Use when repository evidence directly supports the claim.

### High-Risk Signals

Use when the structure strongly suggests a weakness, but the repository does not declare enough contract detail to prove it completely.

### Reviewability Gaps

Use when the repository is too implicit to assess reliably and that lack of explicit structure is itself a maintainability problem.

Missing or uncertain parse evidence that prevents reliable review should also be reported here rather than filled in with a fresh repo-wide inventory.

## Suggestion Rules

- Prefer the smallest explicit boundary improvement that would remove the ambiguity.
- Suggest contract additions before broad rewrites.
- When a component is overloaded, suggest a split along responsibility boundaries.
- When a handoff is vague, suggest an explicit expected output and completion signal.
- When shared state is implicit, suggest declaring reads and writes at the artifact boundary.

## Final Report Rules

- Sort findings by severity first.
- Present the highest-priority findings rather than dumping every review note verbatim.
- Keep evidence concrete and repo-specific.
- Explain why each issue matters for orchestration stability or maintainability.
- Do not pad the report with style comments.
- Stay within contract, flow, and pattern scope rather than broad codebase critique.
