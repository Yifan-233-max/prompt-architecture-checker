# Prompt Architecture Checker

A design-first repository for a prompt-as-code architecture checker.

This project reviews complex prompt-driven, multi-agent systems in the same way linters, static analyzers, and architecture review tools validate codebases. It also includes a prompt architecture reviewer skill and fixture repositories for repository-level review of prompt-as-code systems.

## Problem

Prompt-driven systems accumulate execution logic without a stable syntax layer. That flexibility is useful, but it also creates failure modes that are hard to detect early:

- conflicting instructions across orchestrators, agents, and skills
- missing handoff contracts between agents
- resource acquisition without guaranteed release
- broken file, memory, or artifact references
- prompt steps that exceed context budgets
- ambiguous completion criteria and unverifiable outcomes

## Goal

Build a checker that can:

1. Use AI to interpret a prompt-as-code repository into a structure summary and relationship graph.
2. Review that structure for high-value architecture issues such as weak handoffs, graph problems, and implicit state dependencies.
3. Produce a final report that combines repository structure, findings, and suggested fixes.
4. Evolve toward deterministic lint and workflow simulation after the first slice proves the core value.

## First Scope

The first version focuses on AI-assisted structure understanding and focused architecture review:

- repository structure summary
- call / handoff relationship graph
- review of handoff, graph, and implicit state issues
- markdown report output
- evidence and uncertainty annotations

## Included Reviewer Skill Assets

- `SKILL.md`: public skill entrypoint and pipeline contract
- `src/prompt_architecture_checker/assets/skills/parse-skill/SKILL.md`
- `src/prompt_architecture_checker/assets/skills/review-skill/SKILL.md`
- `src/prompt_architecture_checker/assets/skills/report-skill/SKILL.md`
- `examples/good-repo/`, `examples/bad-repo/`, `examples/mixed-repo/`: repository review fixtures and expected outputs

## Pipeline Contract

- `parse` is the ONLY stage that reads repository files. It produces
  `summary`, `graph`, `evidence`, `uncertainties`.
- `review` consumes the parse artifact and MUST NOT re-read the repository.
  Every finding cites parse evidence or is marked `reviewability-gap`.
- `report` consumes parse + review and renders a prioritized markdown report.
  It MUST NOT re-read the repository.

## Repository Layout

- `SKILL.md`: skill entrypoint and pipeline contract
- `src/prompt_architecture_checker/`: Python CLI implementation
- `src/prompt_architecture_checker/assets/skills/`: per-stage SKILL.md assets bundled with the wheel
- `schemas/prompt-contract.schema.json`: minimal machine-readable contract schema
- `docs/vision.md`: product vision and architecture
- `docs/lint-rules.md`: candidate future deterministic lint rules
- `examples/`: fixture repositories and sample parse / review / report outputs

## Suggested Reading Order

1. `README.md` for repository purpose and quick usage
2. `SKILL.md` for the pipeline contract
3. The three per-stage `SKILL.md` files under `src/prompt_architecture_checker/assets/skills/`
4. `docs/vision.md` for product direction and architecture framing
5. `examples/` for fixture repositories and expected outputs

## Review Output Contract

Every finding includes:

- severity: `error` | `warning` | `info`
- findingClass: `confirmed` | `high-risk-signal` | `reviewability-gap`
- category: `contract` | `flow` | `pattern`
- artifactScope
- message
- evidence
- whyItMatters
- suggestedFix

## Non-Goals

- replacing natural-language prompts with a rigid DSL
- enforcing writing style or tone as a primary quality gate
- executing external tools as part of future deterministic lint unless explicitly enabled

## Suggested Product Path

1. Ship the parse / review / report first slice.
2. Add deterministic lint once the parse artifact stabilizes.
3. Add CI integration as a GitHub Action.
4. Consider workflow simulation after graph and review maturity.

## Experimental CLI

The repository ships an experimental Python 3.12+ CLI that shells out to the local GitHub Copilot CLI (`copilot`) as its stage runner.

### Install

Three options, pick one:

1. **From a GitHub Release (no repo checkout required)**

   Grab the wheel URL from the latest release and install directly:

   ```bash
   pip install https://github.com/Yifan-233-max/prompt-architecture-checker/releases/latest/download/prompt_architecture_checker-0.1.0-py3-none-any.whl
   ```

2. **From PyPI** (once the project publishes there)

   ```bash
   pip install prompt-architecture-checker
   ```

3. **Editable from a local clone** (for contributors)

   ```bash
   git clone https://github.com/Yifan-233-max/prompt-architecture-checker.git
   cd prompt-architecture-checker
   python -m pip install -e .[dev]
   ```

The skill assets (`parse` / `review` / `report` prompts) are bundled inside the wheel, so installations from the release wheel or PyPI do **not** require a repo checkout.

### Prerequisites

The default runner invokes the GitHub Copilot CLI in non-interactive mode
(`copilot -p ... --allow-all-tools --no-color -s`). Install it from
<https://github.com/github/copilot-cli> and make sure `copilot` is on `PATH`.

### Run

```bash
prompt-architecture-checker parse  path/to/target-repo --out parse.md
prompt-architecture-checker review path/to/target-repo --out review.md
prompt-architecture-checker report path/to/target-repo --out report.md
```

Or, equivalently, as a module:

```bash
python -m prompt_architecture_checker report path/to/target-repo --out report.md
```

`review` and `report` rerun earlier stages internally. `--out` is optional; when omitted the markdown is printed to stdout only.

### Runner configuration

Override the runner command either via an environment variable:

```bash
set PAC_COPILOT_BIN=copilot
```

or in a `prompt-architecture-checker.toml` file in the working directory:

```toml
[runner]
command = "copilot"
```
