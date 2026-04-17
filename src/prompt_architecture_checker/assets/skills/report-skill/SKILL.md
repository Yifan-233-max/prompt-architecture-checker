# Report Skill

## Purpose

Produce the final human-readable markdown report by combining the Parse and
Review artifacts. You MUST NOT read repository files.

## Input

- Parse artifact: `summary`, `graph`, `evidence`, `uncertainties`
- Review artifact: `findings[]`

## Ordering

Sort findings by:

1. `severity`: error > warning > info
2. `findingClass`: confirmed > high-risk-signal > reviewability-gap
3. `category`: contract > flow > pattern

## Selection

- Include every `error` finding.
- Include every `warning` finding.
- Include `info` findings only when fewer than 10 findings exist in total.
- If more than 15 findings would be included, keep the top 15 by the ordering
  above and state in Section 3 that the list was truncated.

## Report Structure

Use EXACTLY these sections, in this order:

```md
# Prompt Architecture Review

## 1. Repository Structure
<bullet list derived from parse `summary`>

## 2. Relationship Graph
<bullet list derived from parse `graph`. Mark edges without backing evidence with `(unverified)`.>

## 3. Findings
<for each selected finding, render the block below>

### {severity}: {category} — {artifactScope}
- **Class:** {findingClass}
- **Issue:** {message}
- **Evidence:** {evidence joined with "; "}
- **Why it matters:** {whyItMatters}
- **Suggested fix:** {suggestedFix}

## 4. Reviewability Gaps
<list every `reviewability-gap` finding here so maintainers see what must be made explicit before the next review>

## 5. Next Step
<one sentence recommending the single highest-leverage fix>
```

## Hard Rules

- Output markdown only. No preamble, no trailing commentary, no code fence
  wrapping the whole output.
- Do NOT invent findings that are not present in the review artifact.
- Do NOT read repository files.
- If the review artifact is empty, output Sections 1, 2, 4, and 5 and state
  "No findings" in Section 3.
