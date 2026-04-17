# Review Skill

## Purpose

Assess a Parse artifact for contract, flow, and pattern weaknesses.
You MUST NOT read repository files. The Parse artifact is the sole input.

## Input

The caller provides a Parse artifact with `summary`, `graph`, `evidence`,
and `uncertainties`.

## Review Procedure

1. Classify every graph edge and summary entry as:
   - **evidence-backed** — a matching `evidence` entry exists, or
   - **inferred only** — no `evidence` backing.
2. Apply the three lenses below to evidence-backed items.
3. For inferred-only items or items blocked by `uncertainties`, raise
   `reviewability-gap` findings instead of guessing runtime behavior.
4. Merge duplicate findings; keep the one with the strongest evidence.

## Lenses

### Contract Lens
- handoffs with no declared expected output
- state writes that are implicit instead of declared
- completion criteria that cannot be verified
- referenced files, artifacts, or memory paths that do not close the loop

### Flow Lens
- success paths with no declared downstream consumer
- failure paths missing cleanup or evidence capture
- release or reporting steps not reachable from all important paths
- ordering that is implied only by prose

### Pattern Lens
- orchestrators owning too many responsibilities
- hidden coupling through shared memory or global artifacts
- helpers that rely on unstated context
- collapsed layering of planning, execution, and reporting
- cycles between collaborators with no explicit bound

## Finding Class Decision Rule

| If … | use findingClass |
| --- | --- |
| parse `evidence` directly supports the claim | `confirmed` |
| structure strongly suggests a weakness but evidence is partial | `high-risk-signal` |
| parse is too implicit, or an `uncertainty` blocks judgment | `reviewability-gap` |

## Severity Rule

- `error`   — likely correctness or orchestration breakage
- `warning` — meaningful design weakness with future risk
- `info`    — explicitness improvement that would strengthen reviewability

## Suggestion Rules

- Prefer the smallest explicit-boundary change that removes the ambiguity.
- Suggest contract additions before broad rewrites.
- For overloaded components, suggest a split along responsibility boundaries.
- For vague handoffs, suggest an explicit expected output and completion signal.
- For implicit shared state, suggest declaring reads and writes at the boundary.

## Output Contract

Return JSON only with this exact shape:

```json
{
  "findings": [
    {
      "severity": "error|warning|info",
      "findingClass": "confirmed|high-risk-signal|reviewability-gap",
      "category": "contract|flow|pattern",
      "artifactScope": "path or subsystem from the parse artifact",
      "message": "one-sentence issue",
      "evidence": ["parse-artifact citation or parse field reference"],
      "whyItMatters": "impact on orchestration or maintainability",
      "suggestedFix": "smallest useful change"
    }
  ]
}
```

## Hard Rules

- Do NOT read repository files; work only from the parse artifact.
- Every `confirmed` finding MUST cite at least one parse `evidence` item.
- Every `reviewability-gap` finding MUST name the missing parse structure.
- Do NOT emit style or tone comments.
- Do NOT invent findings that cannot be tied to the parse artifact.
