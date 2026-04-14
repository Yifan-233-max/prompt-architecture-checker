# Prompt Architecture Reviewer Skill Design

## Summary

Design a repository-level reviewer skill for prompt-as-code projects.

The skill reviews the full repository for architecture, contract, and workflow weaknesses, then returns a severity-ranked findings list with evidence and concrete modification suggestions. It is intentionally design-first: it should help maintainers find structural risks before runtime rather than automate execution.

## Why This Fits The Repository

This repository treats prompt artifacts as executable design assets that should be checked the same way codebases are checked for architecture and workflow correctness.

The proposed skill aligns with that direction by:

- preserving natural-language prompts instead of forcing a rigid DSL
- making boundaries explicit at agent, skill, and workflow handoffs
- separating fact-based structural checks from higher-judgment design review
- prioritizing architecture and workflow correctness over writing style

## Goals

1. Review an entire prompt-as-code repository rather than a single file.
2. Build a clear structural view of the repository before making judgments.
3. Detect contract, handoff, and workflow weaknesses that are likely to break or destabilize orchestration.
4. Detect architecture-pattern weaknesses such as over-centralization, hidden coupling, and unclear responsibility boundaries.
5. Produce a severity-ranked findings list with specific evidence and modification guidance.

## Non-Goals

- runtime execution of workflows or external tools
- full workflow simulation as the primary analysis mode
- broad security scanning as a primary first-version objective
- style, tone, or prompt-writing polish
- automatic code or prompt rewriting

## Primary User And Trigger

The primary user is a maintainer who already has a prompt-as-code repository and wants an architecture review before running or scaling it.

The primary trigger is repository review during design or authoring, especially before the repository is treated as stable enough for wider reuse or future checker automation.

## Recommended Approach

Use a hybrid reviewer with two analysis lanes:

1. **Contract-first review lane** for structure, boundaries, and handoffs.
2. **Pattern-review lane** for system shape, coupling, and responsibility design.

This is preferred over a pure pattern reviewer because it produces more evidence-backed, repairable findings. It is preferred over a pure flow simulator because it remains useful even when repositories have incomplete workflow declarations.

## High-Level Architecture

### 1. Repository Scanner

Scans the repository and identifies review-relevant artifacts such as instructions, agents, skills, workflows, memory definitions, artifacts, and routing or handoff hints.

Its job is to establish what exists and where the likely control boundaries are.

### 2. Contract Mapper

Normalizes each discovered artifact into a common review shape:

- responsibility
- inputs
- outputs
- state reads
- state writes
- allowed or implied tools
- completion signals
- downstream handoffs

The mapper should explicitly distinguish between:

- **declared facts** found directly in the repository
- **inferred facts** that are strongly suggested by structure or wording

That distinction is important because missing declarations are themselves review signals.

### 3. Pattern Reviewer

Evaluates how the repository is organized once the normalized structure exists.

It focuses on issues such as:

- orchestrators that own too many responsibilities
- hidden coupling through shared memory or implicit context
- handoffs that depend on unstated knowledge
- outputs that are never consumed
- unclear layering between planning, execution, and reporting
- cyclical collaboration patterns without clear bounds

### 4. Findings Synthesizer

Merges contract findings and pattern findings into one results model.

Its job is to:

- de-duplicate overlapping findings
- assign severity
- preserve evidence
- prioritize the most dangerous or system-wide issues first

### 5. Suggestion Writer

Writes repair-oriented guidance for high-value findings.

Suggestions should prefer explicit architecture changes such as:

- add a missing expected output to a handoff
- declare state writes instead of relying on implicit memory use
- split an overloaded orchestrator into narrower responsibilities
- make completion evidence explicit for a workflow step

## Analysis Flow

1. Scan the repository and identify major artifacts and likely subsystem boundaries.
2. Build a structural inventory without making evaluative claims yet.
3. Map each important artifact into the normalized contract view.
4. Run contract-oriented analysis for missing, weak, or contradictory boundaries.
5. Run pattern-oriented analysis for responsibility, coupling, and collaboration problems.
6. Merge, de-duplicate, and severity-rank the findings.
7. Generate concrete modification suggestions tied to evidence.

The key principle is:

**establish facts first, then judge patterns, then recommend changes**

That prevents the skill from becoming a vague architecture commentator with weak grounding.

## Findings Model

Each finding should include at least:

- `severity`
- `category`
- `artifactScope`
- `message`
- `evidence`
- `whyItMatters`
- `suggestedFix`

### Categories

- `contract`
- `flow` for weaknesses visible from declared or strongly inferable workflow paths
- `pattern`

### Severity

- `error`: a correctness or orchestration risk likely to break or destabilize behavior
- `warning`: a maintainability or architecture weakness with meaningful future risk
- `info`: a clarity or explicitness improvement that would strengthen reviewability

## Expected Output Shape

The final output should read like a repository review report, not a freeform essay.

The most important section is a prioritized findings list where the most severe issues appear first and each issue is backed by concrete repository evidence.

The tone should be decisive when evidence is strong and explicit when the skill is inferring risk rather than proving failure.

## Error Handling And Uncertainty

The skill should never pretend repository evidence is stronger than it is.

It must distinguish between:

1. **confirmed findings** backed by explicit repository evidence
2. **high-risk signals** where the structure strongly suggests a weakness but the contract is incomplete
3. **reviewability gaps** where the repository is too implicit to assess reliably

If the repository lacks enough explicit workflow or contract information, the correct outcome is not silent confidence. The correct outcome is a finding that the repository is difficult to review because key boundaries are missing or implicit.

## Testing Strategy

Testing should focus on whether the skill surfaces the right classes of architecture problems, not whether it produces a specific phrase.

Use example repositories or fixtures that cover:

- a well-structured repository with explicit contracts and clean handoffs
- a repository with hidden dependencies, overloaded orchestrators, and unclear completion
- a repository with mixed-quality areas where some issues are certain and others are only risk signals

Success criteria:

1. The skill consistently identifies the main architecture artifacts.
2. It separates deterministic structure problems from higher-judgment pattern problems.
3. It ranks serious repository-wide weaknesses ahead of minor clarity issues.
4. Its suggestions point back to specific boundary changes rather than generic advice.

## Trade-Offs And Decisions

### Why not pattern-first?

Pattern-first review is easier to discuss, but it produces more subjective output and weaker links between findings and repair steps.

### Why not simulation-first?

Simulation-first review is strong for explicit workflows, but many prompt-as-code repositories do not declare enough flow structure to make it the most stable first lens.

### Why this hybrid?

The contract-first lane gives the skill a hard structural backbone. The pattern lane adds the higher-level architectural judgment needed to catch design issues that are not visible from field presence alone.

That combination best matches the repository's thesis: thin syntax, strong validation, explicit boundaries, and design review before runtime.
