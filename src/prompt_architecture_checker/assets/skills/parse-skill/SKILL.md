# Parse Skill

Analyze the repository at the provided path.

Return JSON only with this exact shape:

```json
{
  "summary": ["..."],
  "graph": ["source -> target"],
  "evidence": ["..."],
  "uncertainties": ["..."]
}
```
