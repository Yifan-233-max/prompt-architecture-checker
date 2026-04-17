# Review Skill

Review the provided parse artifact and return findings only in the following categories:

- contract
- flow
- pattern

Return JSON only with this exact shape:

```json
{
  "findings": [
    {
      "severity": "warning",
      "findingClass": "high-risk-signal",
      "category": "flow",
      "artifactScope": "path/to/file",
      "message": "One-sentence issue",
      "evidence": ["Concrete evidence"],
      "whyItMatters": "Why this matters",
      "suggestedFix": "Smallest useful fix"
    }
  ]
}
```
