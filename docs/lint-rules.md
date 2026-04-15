# Initial Lint Rules

This document lists candidate future deterministic lint rules for Prompt Architecture Checker.

The first implementation slice is centered on `parse`, `review`, and `report`, so the rules below are roadmap material rather than the first delivered capability.

## Contract Rules

1. Every orchestrator handoff must declare expected output.
2. Every agent must declare allowed tools or explicit inheritance.
3. Every workflow step must define a completion signal or evidence artifact.
4. Every state write target must be declared in contract metadata.
5. Every referenced file, memory path, or artifact path must resolve.

## Flow Rules

6. Every acquire step that locks or reserves a resource must have a release path.
7. Every release step must be reachable from both success and failure paths.
8. No route should match two handlers without a precedence rule.
9. A workflow should not dispatch an agent whose output is never consumed.
10. Cycles between agents must be explicit and bounded.

## Tooling Rules

11. A child agent must not use tools forbidden by parent or global policy.
12. High-cost tools must be marked as context-expensive or rate-limited.
13. Browser or UI steps should declare retry policy and evidence capture behavior.
14. External side effects should require explicit confirmation policy.

## Prompt Quality Rules

15. Instructions must not contain contradictory termination conditions.
16. Failure handling must specify retry, escalate, or abort behavior.
17. Prompts with required templates must not drift from canonical form.
18. Handoffs must not rely on hidden knowledge not present in files or state.

## Observability Rules

19. Reports must identify the artifact or step that produced each major outcome.
20. Critical workflows must emit enough evidence to debug failures post hoc.

## Severity Model

- `error`: correctness or safety issue likely to break execution
- `warning`: architecture weakness or maintainability risk
- `info`: improvement opportunity or missing clarity

## Example Finding Format

```json
{
  "ruleId": "flow.acquire-release-symmetry",
  "severity": "error",
  "message": "Session resource is acquired but not guaranteed to be released on failure.",
  "file": ".github/instructions/orchestration.instructions.md",
  "location": {
    "line": 42
  },
  "suggestion": "Add an explicit failure-path release step or finally-style cleanup instruction."
}
```
