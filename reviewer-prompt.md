# Detailed Reviewer Prompt

## Purpose

Review a prompt-as-code repository for contract, flow, and architecture-pattern weaknesses before runtime.

## Review Sequence

1. Read the repository tree and primary documentation.
2. Build an inventory of orchestrators, agents, skills, workflows, memory references, artifacts, and routing hints.
3. Separate explicit declarations from inferred structure.
4. Review the repository through the contract, flow, and pattern lenses below.
5. Merge overlapping findings and rank them by severity.
6. Produce concrete repair suggestions tied to evidence.

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

## Suggestion Rules

- Prefer the smallest explicit boundary improvement that would remove the ambiguity.
- Suggest contract additions before broad rewrites.
- When a component is overloaded, suggest a split along responsibility boundaries.
- When a handoff is vague, suggest an explicit expected output and completion signal.
- When shared state is implicit, suggest declaring reads and writes at the artifact boundary.

## Final Report Rules

- Sort findings by severity first.
- Keep evidence concrete and repo-specific.
- Explain why each issue matters for orchestration stability or maintainability.
- Do not pad the report with style comments.
