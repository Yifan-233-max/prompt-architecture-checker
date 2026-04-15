# Output Format

## Required Fields

| Field | Meaning |
| --- | --- |
| `severity` | `error`, `warning`, or `info` |
| `findingClass` | `confirmed`, `high-risk-signal`, or `reviewability-gap` |
| `category` | `contract`, `flow`, or `pattern` |
| `artifactScope` | File, directory, or subsystem affected by the finding |
| `message` | One-sentence summary of the issue |
| `evidence` | Concrete repository evidence supporting the claim |
| `whyItMatters` | Why the issue affects orchestration or maintainability |
| `suggestedFix` | The smallest high-value change that reduces the risk |

## Markdown Report Template

```md
## Findings

### Error

1. **[category]** `artifactScope`
   - **Class:** findingClass
   - **Issue:** message
   - **Evidence:** evidence
   - **Why it matters:** whyItMatters
   - **Suggested fix:** suggestedFix
```

## JSON Example

```json
{
  "severity": "error",
  "findingClass": "confirmed",
  "category": "contract",
  "artifactScope": "workflows/release.instructions.md",
  "message": "The publish handoff has no declared expected output.",
  "evidence": [
    "The workflow hands off to publish-agent but does not define what artifact or state update should come back."
  ],
  "whyItMatters": "Downstream steps cannot verify whether publishing completed or failed cleanly.",
  "suggestedFix": "Add an explicit expected output such as a release artifact path or status update contract."
}
```

## Severity Rules

- `error`: likely correctness or orchestration breakage
- `warning`: meaningful design weakness with future risk
- `info`: explicitness improvement that would strengthen reviewability
