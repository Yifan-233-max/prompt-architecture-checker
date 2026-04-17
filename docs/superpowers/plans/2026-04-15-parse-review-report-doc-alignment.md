# Parse / Review / Report Doc Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Realign this repository's public docs and examples so the first-version story is clearly centered on `parse`, `review`, and `report`.

**Architecture:** Keep the long-term checker vision intact, but rewrite first-scope messaging so it no longer presents `lint`, `simulate`, or a separate `graph` subsystem as first-version pillars. Add lightweight example outputs that show what `parse`, `review`, and `report` are supposed to produce without introducing implementation code.

**Tech Stack:** Markdown, JSON, Git, ripgrep

---

## File Structure

- `README.md` — public first-impression document; must describe the first version as `parse` / `review` / `report`
- `docs/vision.md` — product framing doc; should preserve the long-term thesis while clearly separating the first product slice from future modes
- `docs/lint-rules.md` — future deterministic-rule backlog; should no longer read like the immediate first deliverable
- `examples/sample-orchestrator.contract.json` — existing sample contract that the new example outputs will explain and review
- `examples/sample-parse-summary.md` — example human-readable output for `parse`
- `examples/sample-review-findings.md` — example focused findings output for `review`
- `examples/sample-report.md` — example final markdown output for `report`

### Task 1: Rewrite `README.md` Around the First Slice

**Files:**
- Modify: `README.md`
- Test: `README.md`

- [ ] **Step 1: Prove the current README still advertises the broader first scope**

Run:

```bash
rg "^- `parser`:|^- `graph`:|^- `lint`:|^- `simulate`:|^## First Scope$|^## Proposed Components$" README.md -n
```

Expected: matches for the old component list and the existing first-scope section.

- [ ] **Step 2: Replace the `## Goal` section**

Replace the current `## Goal` block with:

```md
## Goal

Build a checker that can:

1. Use AI to interpret a prompt-as-code repository into a structure summary and relationship graph.
2. Review that structure for high-value architecture issues such as weak handoffs, graph problems, and implicit state dependencies.
3. Produce a final report that combines repository structure, findings, and suggested fixes.
4. Evolve toward deterministic lint and workflow simulation after the first slice proves the core value.
```

- [ ] **Step 3: Replace the `## First Scope` section**

Replace the current `## First Scope` block with:

```md
## First Scope

The first version focuses on AI-assisted structure understanding and focused architecture review:

- repository structure summary
- call / handoff relationship graph
- review of handoff, graph, and implicit state issues
- markdown report output
- evidence and uncertainty annotations
```

- [ ] **Step 4: Replace the `## Proposed Components` section**

Replace the current `## Proposed Components` block with:

```md
## Proposed Components

- `parse`: interprets a prompt-as-code repository and produces a structure summary plus relationship graph
- `review`: analyzes parse output for high-value architecture issues
- `report`: produces the final structure-and-findings report
```

- [ ] **Step 5: Update `## Repository Layout` and `## Suggested Product Path`**

Update the `examples/` bullet in `## Repository Layout` to:

```md
- `examples/`: example prompt-as-code structures, contract snippets, and sample parse / review / report outputs
```

Replace the current `## Suggested Product Path` block with:

```md
## Suggested Product Path

1. Ship the parse / review / report first slice.
2. Add deterministic lint once the parse artifact stabilizes.
3. Add CI integration as a GitHub Action.
4. Consider workflow simulation after graph and review maturity.
```

- [ ] **Step 6: Verify the new README wording is present and the old first-scope component list is gone**

Run:

```bash
rg "^- `parse`:|^- `review`:|^- `report`:|^1\\. Ship the parse / review / report first slice\\.$|^2\\. Add deterministic lint once the parse artifact stabilizes\\.$" README.md -n
```

Expected: 5 matches proving the new component list and product path are present.

Run:

```bash
rg "^- `parser`:|^- `graph`:|^- `lint`:|^- `simulate`:" README.md -n
```

Expected: no matches, proving the old top-level first-scope component list is gone.

- [ ] **Step 7: Commit the README scope rewrite**

Run:

```bash
git add README.md
git commit -m "docs: refocus readme on parse review report" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that changes only `README.md`.

### Task 2: Align `docs/vision.md` and `docs/lint-rules.md`

**Files:**
- Modify: `docs/vision.md`
- Modify: `docs/lint-rules.md`
- Test: `docs/vision.md`
- Test: `docs/lint-rules.md`

- [ ] **Step 1: Prove `docs/vision.md` still describes modes as `Lint`, `Review`, and `Simulate` only**

Run:

```bash
rg "^## Checker Modes$|^### Lint$|^### Review$|^### Simulate$" docs/vision.md -n
```

Expected: 4 matches, proving the vision doc still presents the older mode framing.

- [ ] **Step 2: Replace the `## Checker Modes` section in `docs/vision.md`**

Replace the current `## Checker Modes` section with:

```md
## First Product Slice

### Parse
AI-assisted repository interpretation for structure summary, call flow, handoff graph, evidence, and uncertainty markers.

### Review
Focused analysis of parse output for handoff and completion problems, graph problems, and implicit state dependencies.

### Report
Human-readable markdown that combines structure summary, key relationship graph, prioritized findings, and suggested fixes.

## Future Modes

### Lint
Deterministic checks for missing files, broken references, route conflicts, undeclared writes, missing cleanup, and contract inconsistencies after the parse artifact stabilizes.

### Simulate
Flow analysis to validate resource acquisition and release symmetry, step reachability, and evidence generation expectations after graph and review maturity.
```

- [ ] **Step 3: Replace the `## Output Targets` section in `docs/vision.md`**

Replace the current `## Output Targets` block with:

```md
## Output Targets

- human-readable markdown report as the primary first-version surface
- thin structured parse / review artifact used internally between commands
- JSON or SARIF as later outputs once the first slice stabilizes
```

- [ ] **Step 4: Add a first-slice disclaimer under `# Initial Lint Rules` in `docs/lint-rules.md`**

Insert these two paragraphs directly below the title:

```md
This document lists candidate future deterministic lint rules for Prompt Architecture Checker.

The first implementation slice is centered on `parse`, `review`, and `report`, so the rules below are roadmap material rather than the first delivered capability.
```

- [ ] **Step 5: Verify the aligned wording exists in both docs**

Run:

```bash
rg "^## First Product Slice$|^### Parse$|^### Review$|^### Report$|^## Future Modes$|^### Lint$|^### Simulate$|^## Output Targets$" docs/vision.md -n
```

Expected: 8 matches proving the new first-slice and future-mode structure exists.

Run:

```bash
rg "^This document lists candidate future deterministic lint rules for Prompt Architecture Checker\\.$|^The first implementation slice is centered on `parse`, `review`, and `report`, so the rules below are roadmap material rather than the first delivered capability\\.$" docs/lint-rules.md -n
```

Expected: 2 matches proving the lint-rules disclaimer is present.

- [ ] **Step 6: Commit the vision and lint-roadmap alignment**

Run:

```bash
git add docs/vision.md docs/lint-rules.md
git commit -m "docs: align vision with first product slice" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that changes only the two docs files.

### Task 3: Add Example Outputs for `parse`, `review`, and `report`

**Files:**
- Create: `examples/sample-parse-summary.md`
- Create: `examples/sample-review-findings.md`
- Create: `examples/sample-report.md`
- Test: `examples/sample-parse-summary.md`
- Test: `examples/sample-review-findings.md`
- Test: `examples/sample-report.md`

- [ ] **Step 1: Create `examples/sample-parse-summary.md`**

```md
# Sample Parse Summary

## Repository Structure

- Primary artifact: `examples/sample-orchestrator.contract.json`
- Identified role: `ui-test-orchestrator` (`orchestrator`)
- Purpose: Coordinates CPC acquisition, UI execution, reporting, and release

## Likely Entrypoint

- `ui-test-orchestrator`

## Key Relationships

1. `ui-test-orchestrator` -> `cpc-connector` after `ACQUIRE`
2. `ui-test-orchestrator` -> `report-generator` after `EXECUTE`

## State And Artifact Signals

- reads `config/resource-pool.json`
- reads `/memories/session/test-state-session-N.md`
- writes `/memories/session/test-state-session-N.md`
- writes `reports/test-run.html`
- produces `evidence/session-N/`

## Evidence

- `handoffs` defines the `cpc-connector` and `report-generator` flow edges
- `completion` defines `Report file exists` and `Session resources released`

## Uncertainties

- failure-path cleanup is implied by the completion list, but it is not modeled as a separate explicit flow edge
```

- [ ] **Step 2: Create `examples/sample-review-findings.md`**

```md
# Sample Review Findings

## Findings

### Info

1. **contract** `examples/sample-orchestrator.contract.json`
   - **Class:** confirmed
   - **Issue:** The orchestrator declares explicit inputs, outputs, state usage, completion signals, and handoffs.
   - **Evidence:** `inputs`, `outputs`, `reads`, `writes`, `completion`, and `handoffs` are all present in the contract.
   - **Why it matters:** This makes the repository easier to interpret and review.
   - **Suggested fix:** Keep future orchestrator contracts at the same level of explicitness.

### Warning

1. **flow** `examples/sample-orchestrator.contract.json`
   - **Class:** high-risk-signal
   - **Issue:** The contract makes success-path handoffs explicit, but it does not model a distinct failure-path release flow.
   - **Evidence:** The contract includes success-oriented handoffs and a completion item `Session resources released`, but no separate failure-path edge or cleanup step.
   - **Why it matters:** Reviewers can infer cleanup intent, but cannot verify failure-path symmetry from the graph alone.
   - **Suggested fix:** Add an explicit cleanup or failure-path handoff in future workflow examples when modeling release-sensitive flows.
```

- [ ] **Step 3: Create `examples/sample-report.md`**

```md
# Sample Report

## Repository Structure Summary

The repository centers on `ui-test-orchestrator`, which coordinates CPC acquisition, UI execution, reporting, and release.

## Key Relationship Graph

1. `ui-test-orchestrator` -> `cpc-connector` after `ACQUIRE`
2. `ui-test-orchestrator` -> `report-generator` after `EXECUTE`

## Highest-Priority Findings

### Warning

1. **flow** `examples/sample-orchestrator.contract.json`
   - **Class:** high-risk-signal
   - **Issue:** The contract makes success-path handoffs explicit, but it does not model a distinct failure-path release flow.
   - **Evidence:** The contract includes success-oriented handoffs and a completion item `Session resources released`, but no separate failure-path edge or cleanup step.
   - **Why it matters:** Reviewers can infer cleanup intent, but cannot verify failure-path symmetry from the graph alone.
   - **Suggested fix:** Add an explicit cleanup or failure-path handoff in future workflow examples when modeling release-sensitive flows.

## Suggested Next Fix

- Add an explicit failure-path cleanup or release edge to the example workflow model.
```

- [ ] **Step 4: Verify the example outputs have the expected anchors**

Run:

```bash
rg "^# Sample Parse Summary$|^## Key Relationships$|^## Uncertainties$|^# Sample Review Findings$|^## Findings$|\\*\\*Class:\\*\\*|^# Sample Report$|^## Repository Structure Summary$|^## Key Relationship Graph$|^## Suggested Next Fix$" examples/sample-parse-summary.md examples/sample-review-findings.md examples/sample-report.md -n
```

Expected: 10 matches proving the new parse, review, and report example anchors exist.

- [ ] **Step 5: Verify the existing contract example still parses as JSON**

Run:

```bash
powershell -Command "Get-Content 'examples/sample-orchestrator.contract.json' -Raw | ConvertFrom-Json | Out-Null; Write-Output 'JSON_OK'"
```

Expected: `JSON_OK`

- [ ] **Step 6: Commit the example outputs**

Run:

```bash
git add examples/sample-parse-summary.md examples/sample-review-findings.md examples/sample-report.md
git commit -m "docs: add parse review report examples" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds only the three new example output files.
