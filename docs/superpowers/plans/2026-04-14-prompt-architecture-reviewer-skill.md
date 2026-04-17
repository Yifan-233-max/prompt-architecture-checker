# Prompt Architecture Reviewer Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an open-source repository named `prompt-architecture-reviewer-skill` whose main deliverable is a Copilot-style reviewer skill for prompt-as-code repositories, backed by helper prompts and example review fixtures.

**Architecture:** The new repository ships a single public entrypoint in `SKILL.md`, then keeps the detailed review procedure and output contract in separate Markdown files so the skill stays readable and maintainable. Example prompt-as-code repositories plus expected review outputs act as fixture-style acceptance tests and documentation.

**Tech Stack:** Markdown, Git, ripgrep, MIT-licensed open-source repository structure

---

## File Structure

All paths below are relative to the root of the new `prompt-architecture-reviewer-skill` repository.

- `README.md` — public repository overview, usage, repository layout, and example invocation
- `LICENSE` — MIT license text
- `.gitignore` — keep OS and editor noise out of the repo
- `SKILL.md` — public skill entrypoint with frontmatter, trigger phrases, workflow, and hard gates
- `reviewer-prompt.md` — detailed contract/flow/pattern review procedure
- `output-format.md` — canonical findings fields, severity rules, and example outputs
- `examples/good-repo/README.md` — example repository with explicit contracts and healthy boundaries
- `examples/good-repo/contracts/ui-test-orchestrator.contract.json` — positive contract example
- `examples/bad-repo/README.md` — example repository with hidden dependencies and overloaded orchestration
- `examples/bad-repo/orchestrator.instructions.md` — negative prompt artifact with implicit behavior
- `examples/mixed-repo/README.md` — example repository with partially explicit structure
- `examples/mixed-repo/contracts/release-workflow.contract.json` — mixed-quality contract example
- `examples/good-repo/expected-review.md` — expected reviewer output for the good example
- `examples/bad-repo/expected-review.md` — expected reviewer output for the bad example
- `examples/mixed-repo/expected-review.md` — expected reviewer output for the mixed example

### Task 1: Scaffold the Open-Source Repository Metadata

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `.gitignore`
- Test: `README.md`

- [ ] **Step 1: Prove the repo does not already contain the public metadata files**

Run:

```bash
rg "^# Prompt Architecture Reviewer Skill$|^MIT License$" README.md LICENSE -n
```

Expected: `rg` reports no matches because the files do not exist yet.

- [ ] **Step 2: Write `README.md`**

````md
# Prompt Architecture Reviewer Skill

Review prompt-as-code repositories for contract, flow, and architecture-pattern weaknesses before runtime.

## What This Repository Ships

- `SKILL.md`: the public skill entrypoint
- `reviewer-prompt.md`: the detailed review procedure
- `output-format.md`: the canonical findings model and report shape
- `examples/`: positive, negative, and mixed review fixtures

## What The Skill Reviews

The skill is designed to review an entire prompt-as-code repository and surface:

- missing or weak contracts
- ambiguous or fragile handoffs
- hidden state dependencies
- architecture-pattern weaknesses
- reviewability gaps where the repository is too implicit to assess reliably

## What The Skill Does Not Try To Do

- run the target repository
- rewrite prompts automatically
- act like a broad security scanner
- prioritize tone or style over architecture correctness

## Example Invocation

```text
Review this prompt-as-code repository. Focus on contract, flow, and architecture-pattern issues. Give me a severity-ranked findings list with evidence and suggested fixes.
````

## Repository Layout

- `SKILL.md`
- `reviewer-prompt.md`
- `output-format.md`
- `examples/good-repo/`
- `examples/bad-repo/`
- `examples/mixed-repo/`

## Review Output Contract

Every finding should include:

- severity
- findingClass
- category
- artifactScope
- message
- evidence
- whyItMatters
- suggestedFix

## License

This repository is released under the MIT License.
```

- [ ] **Step 3: Write `LICENSE`**

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 4: Write `.gitignore`**

```gitignore
.DS_Store
Thumbs.db
*.log
```

- [ ] **Step 5: Verify the metadata files contain the expected anchors**

Run:

```bash
rg "^# Prompt Architecture Reviewer Skill$|^## Repository Layout$|^MIT License$|^Thumbs\\.db$" README.md LICENSE .gitignore -n
```

Expected: four matches, one for the README title, one for the README layout section, one for the MIT license heading, and one for the Windows ignore rule.

- [ ] **Step 6: Commit the repository metadata**

Run:

```bash
git add README.md LICENSE .gitignore
git commit -m "docs: scaffold skill repository metadata" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds the repository metadata files.

### Task 2: Create the Public `SKILL.md` Entrypoint

**Files:**
- Create: `SKILL.md`
- Test: `SKILL.md`

- [ ] **Step 1: Prove the skill entrypoint does not exist yet**

Run:

```bash
rg "^name: prompt-architecture-reviewer$|^# Prompt Architecture Reviewer$" SKILL.md -n
```

Expected: `rg` reports no matches because `SKILL.md` does not exist yet.

- [ ] **Step 2: Write `SKILL.md`**

```md
---
name: prompt-architecture-reviewer
description: Review a prompt-as-code repository for contract, flow, and architecture-pattern weaknesses before runtime.
---

# Prompt Architecture Reviewer

Use this skill when a user wants a repository-level review of a prompt-as-code project, agent workflow repository, or multi-file prompt orchestration system.

## Outcome

Return a severity-ranked findings list with evidence and concrete modification suggestions.

## Hard Gates

- Review the repository structure before making conclusions.
- Build a structural inventory of orchestrators, agents, skills, workflows, state, artifacts, and handoffs.
- Separate confirmed findings, high-risk signals, and reviewability gaps.
- Do not claim runtime behavior unless the repository evidence supports it.
- Focus on contract, flow, and architecture-pattern issues before style.

## Workflow

1. Inspect the repository tree and main documentation.
2. Identify the core artifacts and likely subsystem boundaries.
3. Follow `reviewer-prompt.md` for the detailed review procedure.
4. Format the final report using `output-format.md`.

## Required Report Shape

Every finding must include:

- severity
- findingClass
- category
- artifactScope
- message
- evidence
- whyItMatters
- suggestedFix

Sort findings by severity first, then by architectural impact.

## Review Focus

- contract gaps
- weak or ambiguous handoffs
- hidden shared-state coupling
- unclear completion signals
- architecture-pattern weaknesses
- reviewability gaps caused by implicit structure
```

- [ ] **Step 3: Verify the entrypoint exposes the required frontmatter and workflow sections**

Run:

```bash
rg "^name: prompt-architecture-reviewer$|^description: Review a prompt-as-code repository for contract, flow, and architecture-pattern weaknesses before runtime\\.$|^## Workflow$|^## Required Report Shape$|^- findingClass$" SKILL.md -n
```

Expected: five matches, proving the name, description, workflow section, report-shape section, and `findingClass` requirement exist.

- [ ] **Step 4: Commit the skill entrypoint**

Run:

```bash
git add SKILL.md
git commit -m "docs: add public skill entrypoint" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that introduces the public skill interface.

### Task 3: Add the Detailed Review Procedure

**Files:**
- Create: `reviewer-prompt.md`
- Test: `reviewer-prompt.md`

- [ ] **Step 1: Prove the detailed review procedure is not already present**

Run:

```bash
rg "confirmed findings|high-risk signals|reviewability gaps" reviewer-prompt.md -n
```

Expected: `rg` reports no matches because `reviewer-prompt.md` does not exist yet.

- [ ] **Step 2: Write `reviewer-prompt.md`**

```md
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
```

- [ ] **Step 3: Verify the procedure includes the three review lenses and three finding classes**

Run:

```bash
rg "^## Contract Lens$|^## Flow Lens$|^## Pattern Lens$|^### Confirmed Findings$|^### High-Risk Signals$|^### Reviewability Gaps$" reviewer-prompt.md -n
```

Expected: six matches, one for each required section.

- [ ] **Step 4: Commit the detailed review procedure**

Run:

```bash
git add reviewer-prompt.md
git commit -m "docs: add reviewer prompt procedure" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds the detailed review heuristic.

### Task 4: Add the Canonical Findings Format

**Files:**
- Create: `output-format.md`
- Test: `output-format.md`

- [ ] **Step 1: Prove the findings-format document does not exist yet**

Run:

```bash
rg "artifactScope|suggestedFix|severity" output-format.md -n
```

Expected: `rg` reports no matches because `output-format.md` does not exist yet.

- [ ] **Step 2: Write `output-format.md`**

````md
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
````

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
```

- [ ] **Step 3: Verify the field table, markdown template, and JSON example are present**

Run:

```bash
rg "^## Required Fields$|findingClass|artifactScope|suggestedFix|^## Markdown Report Template$|^## JSON Example$|^## Severity Rules$" output-format.md -n
```

Expected: multiple matches proving the field definitions, `findingClass`, report template, JSON example, and severity rules exist.

- [ ] **Step 4: Commit the output-format document**

Run:

```bash
git add output-format.md
git commit -m "docs: add canonical findings format" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds the findings contract.

### Task 5: Add the Positive and Negative Review Fixtures

**Files:**
- Create: `examples/good-repo/README.md`
- Create: `examples/good-repo/contracts/ui-test-orchestrator.contract.json`
- Create: `examples/bad-repo/README.md`
- Create: `examples/bad-repo/orchestrator.instructions.md`
- Test: `examples/good-repo/contracts/ui-test-orchestrator.contract.json`

- [ ] **Step 1: Write `examples/good-repo/README.md`**

```md
# Good Example Repository

This fixture represents a prompt-as-code repository with explicit contracts, bounded orchestration responsibilities, and observable completion signals.

## Characteristics

- explicit inputs and outputs
- declared state reads and writes
- explicit handoffs with expected outputs
- completion criteria tied to evidence
```

- [ ] **Step 2: Write `examples/good-repo/contracts/ui-test-orchestrator.contract.json`**

```json
{
  "name": "ui-test-orchestrator",
  "kind": "orchestrator",
  "description": "Coordinates CPC acquisition, UI execution, reporting, and release.",
  "inputs": [
    {
      "name": "testCasePath",
      "required": true,
      "description": "Path to the requested test case file."
    }
  ],
  "outputs": [
    {
      "name": "reportPath",
      "required": true,
      "description": "Generated report artifact path."
    }
  ],
  "reads": [
    "config/resource-pool.json",
    "/memories/session/test-state-session-N.md"
  ],
  "writes": [
    "/memories/session/test-state-session-N.md",
    "reports/test-run.html"
  ],
  "artifacts": [
    "evidence/session-N/"
  ],
  "allowedTools": [
    "runSubagent",
    "read_file",
    "memory"
  ],
  "completion": [
    "Report file exists",
    "Session resources released"
  ],
  "handoffs": [
    {
      "target": "cpc-connector",
      "condition": "after ACQUIRE",
      "expectedOutput": "Connected CPC and updated state file"
    },
    {
      "target": "report-generator",
      "condition": "after EXECUTE",
      "expectedOutput": "Self-contained HTML report"
    }
  ]
}
```

- [ ] **Step 3: Write `examples/bad-repo/README.md`**

```md
# Bad Example Repository

This fixture represents a repository with hidden dependencies, overloaded orchestration, and weak reviewability.

## Characteristics

- implicit state usage
- vague handoffs
- unclear completion
- multiple responsibilities collapsed into one orchestrator
```

- [ ] **Step 4: Write `examples/bad-repo/orchestrator.instructions.md`**

```md
# Mega Orchestrator

You own acquisition, execution, retry handling, debugging, reporting, and cleanup for the entire run.

Read the usual state file before you start and keep updating it whenever the situation changes.

If a helper can contribute, send it whatever context seems useful and continue once it looks ready.

When work appears complete, make sure somebody produces a report and release anything that should probably be released.

If something goes wrong, do what is reasonable and keep the run moving.
```

- [ ] **Step 5: Verify the positive fixture is explicit and the negative fixture is intentionally vague**

Run:

```bash
rg "\"expectedOutput\"|\"completion\"|usual state file|looks ready|should probably be released" examples/good-repo/contracts/ui-test-orchestrator.contract.json examples/bad-repo/orchestrator.instructions.md -n
```

Expected: matches for `expectedOutput` and `completion` in the good fixture and matches for the vague phrases in the bad fixture.

- [ ] **Step 6: Commit the positive and negative fixtures**

Run:

```bash
git add examples/good-repo examples/bad-repo
git commit -m "docs: add positive and negative review fixtures" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds the first two repository fixtures.

### Task 6: Add the Mixed-Quality Fixture and Expected Review Outputs

**Files:**
- Create: `examples/mixed-repo/README.md`
- Create: `examples/mixed-repo/contracts/release-workflow.contract.json`
- Create: `examples/good-repo/expected-review.md`
- Create: `examples/bad-repo/expected-review.md`
- Create: `examples/mixed-repo/expected-review.md`
- Test: `examples/mixed-repo/expected-review.md`

- [ ] **Step 1: Write `examples/mixed-repo/README.md`**

```md
# Mixed Example Repository

This fixture represents a repository that has some explicit contracts but still leaves important review questions unresolved.

## Characteristics

- some explicit inputs and reads
- partial handoff structure
- missing completion evidence
- ambiguous publish boundary
```

- [ ] **Step 2: Write `examples/mixed-repo/contracts/release-workflow.contract.json`**

```json
{
  "name": "release-workflow",
  "kind": "workflow",
  "description": "Coordinates release review and publishing.",
  "inputs": [
    {
      "name": "releaseBranch",
      "required": true,
      "description": "Branch that should be evaluated for release."
    }
  ],
  "outputs": [],
  "reads": [
    "memories/release-state.md"
  ],
  "writes": [
    "memories/release-state.md"
  ],
  "artifacts": [
    "reports/release-summary.md"
  ],
  "allowedTools": [
    "read_file",
    "runSubagent"
  ],
  "completion": [],
  "handoffs": [
    {
      "target": "publish-agent",
      "condition": "after review"
    }
  ]
}
```

- [ ] **Step 3: Write `examples/good-repo/expected-review.md`**

```md
# Expected Review: Good Example

## Findings

### Info

1. **pattern** `examples/good-repo/`
   - **Class:** confirmed
   - **Issue:** The repository is strongly structured and does not expose obvious contract or flow breakage.
   - **Evidence:** Inputs, outputs, state reads and writes, completion signals, and handoffs are all declared in the orchestrator contract.
   - **Why it matters:** This fixture should demonstrate the low-noise path for the reviewer.
   - **Suggested fix:** No structural change is required; keep future artifacts at the same level of explicitness.
```

- [ ] **Step 4: Write `examples/bad-repo/expected-review.md`**

```md
# Expected Review: Bad Example

## Findings

### Error

1. **contract** `examples/bad-repo/orchestrator.instructions.md`
   - **Class:** confirmed
   - **Issue:** The orchestrator relies on an unstated state file and does not declare its expected outputs.
   - **Evidence:** The instructions say to read "the usual state file" and never identify a concrete output artifact or completion contract.
   - **Why it matters:** Downstream collaborators cannot verify what the orchestrator consumes or produces.
   - **Suggested fix:** Add an explicit contract that names the state file, declared outputs, and completion signals.

### Warning

1. **pattern** `examples/bad-repo/orchestrator.instructions.md`
   - **Class:** confirmed
   - **Issue:** One orchestrator owns acquisition, execution, retry handling, debugging, reporting, and cleanup.
   - **Evidence:** The opening paragraph assigns nearly the entire system lifecycle to a single unit.
   - **Why it matters:** Over-centralization makes failures harder to isolate and turns handoffs into implicit behavior.
   - **Suggested fix:** Split the unit into narrower responsibilities such as coordination, execution, reporting, and cleanup.
```

- [ ] **Step 5: Write `examples/mixed-repo/expected-review.md`**

```md
# Expected Review: Mixed Example

## Findings

### Warning

1. **flow** `examples/mixed-repo/contracts/release-workflow.contract.json`
   - **Class:** high-risk-signal
   - **Issue:** The publish handoff is declared, but the workflow has no expected output or completion signal for that stage.
   - **Evidence:** The handoff names `publish-agent`, but the contract does not define an `expectedOutput` or any completion criteria.
   - **Why it matters:** Reviewers can see the path exists but cannot verify what successful publishing should return.
   - **Suggested fix:** Add an expected publish artifact or status output and declare the evidence that marks the workflow complete.

### Info

1. **contract** `examples/mixed-repo/contracts/release-workflow.contract.json`
   - **Class:** reviewability-gap
   - **Issue:** The workflow declares shared state reads and writes but does not explain the shape of that state.
   - **Evidence:** The contract references `memories/release-state.md` for both reads and writes without any field-level expectations.
   - **Why it matters:** Hidden structure inside shared state increases coupling and makes future reviews less reliable.
   - **Suggested fix:** Describe the state fields or split the shared state into narrower artifacts with clearer ownership.
```

- [ ] **Step 6: Verify all three example repositories have expected review outputs**

Run:

```bash
rg "^# Expected Review:|^## Findings$|\\*\\*Class:\\*\\*|\\*\\*Suggested fix:\\*\\*" examples/good-repo/expected-review.md examples/bad-repo/expected-review.md examples/mixed-repo/expected-review.md -n
```

Expected: matches from all three expected-review files, proving each fixture has a report title, findings section, explicit finding classes, and concrete suggested fixes.

- [ ] **Step 7: Commit the mixed fixture and expected reviews**

Run:

```bash
git add examples/mixed-repo examples/good-repo/expected-review.md examples/bad-repo/expected-review.md
git commit -m "docs: add mixed fixture and expected review outputs" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that completes the fixture set and their acceptance outputs.

### Task 7: Perform the Final Smoke Validation Pass

**Files:**
- Modify: `README.md`
- Test: `SKILL.md`
- Test: `reviewer-prompt.md`
- Test: `output-format.md`

- [ ] **Step 1: Insert a usage flow section into `README.md` directly below `## Repository Layout` and above `## Review Output Contract`**

```md
## Suggested Reading Order

1. `README.md` for repository purpose and quick usage
2. `SKILL.md` for the public skill contract
3. `reviewer-prompt.md` for the detailed review heuristic
4. `output-format.md` for the report shape
5. `examples/` for fixture repositories and expected outputs
```

- [ ] **Step 2: Verify the repository has all required top-level anchors**

Run:

```bash
rg "^# Prompt Architecture Reviewer Skill$|^# Prompt Architecture Reviewer$|^# Detailed Reviewer Prompt$|^# Output Format$|^## Suggested Reading Order$" README.md SKILL.md reviewer-prompt.md output-format.md -n
```

Expected: five matches, one for each main entrypoint or anchor section.

- [ ] **Step 3: Run a whitespace and formatting sanity check**

Run:

```bash
git diff --check
```

Expected: no output, which means there are no trailing-whitespace or malformed diff issues.

- [ ] **Step 4: Commit the final README polish and validation pass**

Run:

```bash
git add README.md
git commit -m "docs: finalize skill repository walkthrough" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a final commit that leaves the repo ready for open-source publication.
