# Parse / Review / Report CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python CLI that exposes `prompt-architecture-checker parse|review|report <repo>` and orchestrates three Copilot-backed skill stages through an experimental subprocess bridge.

**Architecture:** Use a small Python package with an argparse command layer, an experimental GitHub Copilot subprocess runner, stage-specific skill assets, and explicit parse/review/report artifacts. The CLI remains repo-direct for users, but internally it sequences `parse-skill`, `review-skill`, and `report-skill` in order and only writes the invoked command's primary output when `--out` is provided.

**Tech Stack:** Python 3.12, argparse, dataclasses, json, pathlib, subprocess, pytest

---

## File Structure

- `pyproject.toml` — package metadata, editable install config, and console script registration
- `src/prompt_architecture_checker/__init__.py` — package marker and version export
- `src/prompt_architecture_checker/cli.py` — argparse entrypoint and command dispatch
- `src/prompt_architecture_checker/contracts.py` — parse/review/report artifact dataclasses and JSON normalization helpers
- `src/prompt_architecture_checker/config.py` — runner command discovery through config, environment, and defaults
- `src/prompt_architecture_checker/skill_assets.py` — load `parse-skill`, `review-skill`, and `report-skill` prompt assets from disk
- `src/prompt_architecture_checker/prompt_builder.py` — turn repo path and upstream artifacts into stage prompts
- `src/prompt_architecture_checker/runner.py` — experimental Copilot subprocess bridge and runner protocol
- `src/prompt_architecture_checker/orchestrator.py` — `run_parse`, `run_review`, and `run_report` stage sequencing
- `src/prompt_architecture_checker/output.py` — render parse/review/report primary outputs and write `--out`
- `skills/parse-skill/SKILL.md` — parse-stage prompt contract that returns JSON
- `skills/review-skill/SKILL.md` — review-stage prompt contract that returns JSON findings
- `skills/report-skill/SKILL.md` — report-stage prompt contract that returns markdown
- `tests/conftest.py` — sample repo fixture and stub runner factory
- `tests/test_cli_help.py` — parser smoke test
- `tests/test_skill_assets.py` — skill asset loading and artifact normalization tests
- `tests/test_runner.py` — subprocess bridge tests with a fake runner script
- `tests/test_cli_parse.py` — `parse <repo>` terminal behavior and stage invocation
- `tests/test_cli_review.py` — `review <repo>` stage chaining and focused output
- `tests/test_cli_report.py` — `report <repo>` stage chaining and `--out` behavior
- `tests/test_cli_errors.py` — repo validation and stage failure behavior
- `README.md` — installation, usage, and experimental runner note

### Task 1: Scaffold the Python package and CLI surface

**Files:**
- Create: `pyproject.toml`
- Create: `src/prompt_architecture_checker/__init__.py`
- Create: `src/prompt_architecture_checker/cli.py`
- Create: `tests/test_cli_help.py`
- Test: `tests/test_cli_help.py`

- [ ] **Step 1: Write the failing CLI parser test**

```python
from prompt_architecture_checker.cli import build_parser


def test_build_parser_exposes_parse_review_report_subcommands():
    parser = build_parser()
    subparsers_action = next(
        action for action in parser._actions if getattr(action, "choices", None)
    )

    assert set(subparsers_action.choices) == {"parse", "review", "report"}
```

- [ ] **Step 2: Run the parser test to confirm the package does not exist yet**

Run:

```bash
python -m pytest tests/test_cli_help.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'prompt_architecture_checker'`.

- [ ] **Step 3: Create the package metadata and CLI skeleton**

`pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "prompt-architecture-checker"
version = "0.1.0"
description = "CLI entrypoints for parse, review, and report over prompt-as-code repositories."
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0"]

[project.scripts]
prompt-architecture-checker = "prompt_architecture_checker.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

`src/prompt_architecture_checker/__init__.py`

```python
__all__ = ["__version__"]

__version__ = "0.1.0"
```

`src/prompt_architecture_checker/cli.py`

```python
import argparse
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-architecture-checker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("parse", "review", "report"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("repo")
        subparser.add_argument("--out", dest="out_path")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0
```

- [ ] **Step 4: Install the package in editable mode for local test runs**

Run:

```bash
python -m pip install -e .[dev]
```

Expected: editable install completes and registers the `prompt-architecture-checker` console script.

- [ ] **Step 5: Run the parser test to confirm the CLI surface exists**

Run:

```bash
python -m pytest tests/test_cli_help.py -q
```

Expected: PASS with `1 passed`.

- [ ] **Step 6: Commit the scaffold**

Run:

```bash
git add pyproject.toml src/prompt_architecture_checker/__init__.py src/prompt_architecture_checker/cli.py tests/test_cli_help.py
git commit -m "feat: scaffold python cli package" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit containing only the package scaffold and parser smoke test.

### Task 2: Add stage contracts, skill assets, and prompt builders

**Files:**
- Create: `src/prompt_architecture_checker/contracts.py`
- Create: `src/prompt_architecture_checker/skill_assets.py`
- Create: `src/prompt_architecture_checker/prompt_builder.py`
- Create: `skills/parse-skill/SKILL.md`
- Create: `skills/review-skill/SKILL.md`
- Create: `skills/report-skill/SKILL.md`
- Create: `tests/conftest.py`
- Create: `tests/test_skill_assets.py`
- Test: `tests/test_skill_assets.py`

- [ ] **Step 1: Write the failing skill asset and contract tests**

`tests/test_skill_assets.py`

```python
from pathlib import Path

from prompt_architecture_checker.contracts import (
    parse_parse_artifact,
    parse_review_artifact,
)
from prompt_architecture_checker.prompt_builder import build_review_prompt
from prompt_architecture_checker.skill_assets import load_skill_text


def test_load_skill_text_returns_parse_skill_content():
    text = load_skill_text("parse")

    assert "Return JSON only" in text
    assert "summary" in text


def test_parse_artifact_parser_reads_expected_shape():
    artifact = parse_parse_artifact(
        {
            "summary": ["ui-test-orchestrator"],
            "graph": ["ui-test-orchestrator -> report-generator"],
            "evidence": ["examples/sample-orchestrator.contract.json"],
            "uncertainties": ["failure cleanup inferred"],
        }
    )

    assert artifact.summary == ["ui-test-orchestrator"]
    assert artifact.graph == ["ui-test-orchestrator -> report-generator"]


def test_review_artifact_parser_reads_expected_shape():
    artifact = parse_review_artifact(
        {
            "findings": [
                {
                    "severity": "warning",
                    "findingClass": "high-risk-signal",
                    "category": "flow",
                    "artifactScope": "examples/sample-orchestrator.contract.json",
                    "message": "Release flow is not explicit on failure.",
                    "evidence": ["Completion text exists but no failure-path edge is declared."],
                    "whyItMatters": "Cleanup behavior cannot be verified from declared structure.",
                    "suggestedFix": "Add a failure-path cleanup edge.",
                }
            ]
        }
    )

    assert artifact.findings[0].severity == "warning"
    assert artifact.findings[0].category == "flow"


def test_build_review_prompt_embeds_parse_artifact():
    parse_artifact = parse_parse_artifact(
        {
            "summary": ["ui-test-orchestrator"],
            "graph": ["ui-test-orchestrator -> report-generator"],
            "evidence": ["examples/sample-orchestrator.contract.json"],
            "uncertainties": ["failure cleanup inferred"],
        }
    )

    prompt = build_review_prompt(
        Path("repo"),
        load_skill_text("review"),
        parse_artifact,
    )

    assert "Stage: review" in prompt
    assert '"summary": [' in prompt
```

- [ ] **Step 2: Run the tests to verify the new modules are still missing**

Run:

```bash
python -m pytest tests/test_skill_assets.py -q
```

Expected: FAIL with import errors for `contracts`, `skill_assets`, or `prompt_builder`.

- [ ] **Step 3: Create the skill prompt assets**

`skills/parse-skill/SKILL.md`

````md
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
````

`skills/review-skill/SKILL.md`

````md
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
````

`skills/report-skill/SKILL.md`

````md
# Report Skill

Combine the provided parse artifact and review artifact into a final markdown report.

The report must contain:

1. Repository structure summary
2. Key relationship graph
3. Highest-priority findings
4. Suggested next fix

Return markdown only.
````

- [ ] **Step 4: Create the contract, asset loader, prompt builder, and shared test fixtures**

`src/prompt_architecture_checker/contracts.py`

```python
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ParseArtifact:
    summary: list[str]
    graph: list[str]
    evidence: list[str]
    uncertainties: list[str]


@dataclass(frozen=True)
class ReviewFinding:
    severity: str
    finding_class: str
    category: str
    artifact_scope: str
    message: str
    evidence: list[str]
    why_it_matters: str
    suggested_fix: str


@dataclass(frozen=True)
class ReviewArtifact:
    findings: list[ReviewFinding]


@dataclass(frozen=True)
class ReportArtifact:
    markdown: str


def parse_parse_artifact(payload: dict[str, Any]) -> ParseArtifact:
    return ParseArtifact(
        summary=list(payload["summary"]),
        graph=list(payload["graph"]),
        evidence=list(payload["evidence"]),
        uncertainties=list(payload["uncertainties"]),
    )


def parse_review_artifact(payload: dict[str, Any]) -> ReviewArtifact:
    return ReviewArtifact(
        findings=[
            ReviewFinding(
                severity=item["severity"],
                finding_class=item["findingClass"],
                category=item["category"],
                artifact_scope=item["artifactScope"],
                message=item["message"],
                evidence=list(item["evidence"]),
                why_it_matters=item["whyItMatters"],
                suggested_fix=item["suggestedFix"],
            )
            for item in payload["findings"]
        ]
    )
```

`src/prompt_architecture_checker/skill_assets.py`

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_PATHS = {
    "parse": ROOT / "skills" / "parse-skill" / "SKILL.md",
    "review": ROOT / "skills" / "review-skill" / "SKILL.md",
    "report": ROOT / "skills" / "report-skill" / "SKILL.md",
}


def load_skill_text(stage: str) -> str:
    return SKILL_PATHS[stage].read_text(encoding="utf-8")
```

`src/prompt_architecture_checker/prompt_builder.py`

```python
import json
from dataclasses import asdict
from pathlib import Path

from .contracts import ParseArtifact, ReviewArtifact


def build_parse_prompt(repo_path: Path, skill_text: str) -> str:
    return (
        f"{skill_text}\n\n"
        f"Stage: parse\n"
        f"Repository path: {repo_path}\n"
    )


def build_review_prompt(repo_path: Path, skill_text: str, parse_artifact: ParseArtifact) -> str:
    return (
        f"{skill_text}\n\n"
        f"Stage: review\n"
        f"Repository path: {repo_path}\n"
        f"Parse artifact:\n{json.dumps(asdict(parse_artifact), indent=2)}\n"
    )


def build_report_prompt(
    repo_path: Path,
    skill_text: str,
    parse_artifact: ParseArtifact,
    review_artifact: ReviewArtifact,
) -> str:
    return (
        f"{skill_text}\n\n"
        f"Stage: report\n"
        f"Repository path: {repo_path}\n"
        f"Parse artifact:\n{json.dumps(asdict(parse_artifact), indent=2)}\n"
        f"Review artifact:\n{json.dumps(asdict(review_artifact), indent=2)}\n"
    )
```

`tests/conftest.py`

```python
from pathlib import Path

import pytest


class StubRunner:
    def __init__(self, responses: list[str]):
        self.responses = list(responses)
        self.prompts: list[str] = []

    def run(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.responses.pop(0)


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# sample repo\n", encoding="utf-8")
    return repo


@pytest.fixture
def stub_runner_factory():
    def factory(*responses: str) -> StubRunner:
        return StubRunner(list(responses))

    return factory
```

- [ ] **Step 5: Run the new tests to verify the assets and contracts now exist**

Run:

```bash
python -m pytest tests/test_skill_assets.py -q
```

Expected: PASS with `4 passed`.

- [ ] **Step 6: Commit the contracts and skill assets**

Run:

```bash
git add src/prompt_architecture_checker/contracts.py src/prompt_architecture_checker/skill_assets.py src/prompt_architecture_checker/prompt_builder.py skills/parse-skill/SKILL.md skills/review-skill/SKILL.md skills/report-skill/SKILL.md tests/conftest.py tests/test_skill_assets.py
git commit -m "feat: add stage contracts and skill assets" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that introduces the stage asset and artifact foundation.

### Task 3: Build the experimental Copilot subprocess bridge

**Files:**
- Create: `src/prompt_architecture_checker/config.py`
- Create: `src/prompt_architecture_checker/runner.py`
- Create: `tests/test_runner.py`
- Test: `tests/test_runner.py`

- [ ] **Step 1: Write the failing subprocess runner tests**

`tests/test_runner.py`

```python
import sys

import pytest

from prompt_architecture_checker.config import resolve_copilot_command
from prompt_architecture_checker.runner import CopilotCliRunner, RunnerInvocationError


def test_resolve_copilot_command_prefers_env_over_config(tmp_path, monkeypatch):
    config_path = tmp_path / "prompt-architecture-checker.toml"
    config_path.write_text('[runner]\ncommand = "copilot --experimental"\n', encoding="utf-8")
    monkeypatch.setenv("PAC_COPILOT_BIN", "copilot-preview")

    assert resolve_copilot_command(config_path) == ["copilot-preview"]


def test_copilot_runner_returns_stdout_from_subprocess(tmp_path):
    script = tmp_path / "fake_copilot.py"
    script.write_text(
        "import sys\n"
        "prompt = sys.stdin.read()\n"
        "sys.stdout.write(prompt.upper())\n",
        encoding="utf-8",
    )

    runner = CopilotCliRunner(command=[sys.executable, str(script)])

    assert runner.run('Stage: parse') == 'STAGE: PARSE'


def test_copilot_runner_raises_on_nonzero_exit(tmp_path):
    script = tmp_path / "failing_copilot.py"
    script.write_text(
        "import sys\n"
        "sys.stderr.write('runner failed')\n"
        "raise SystemExit(2)\n",
        encoding="utf-8",
    )

    runner = CopilotCliRunner(command=[sys.executable, str(script)])

    with pytest.raises(RunnerInvocationError, match='runner failed'):
        runner.run('Stage: parse')
```

- [ ] **Step 2: Run the runner tests to confirm the bridge does not exist yet**

Run:

```bash
python -m pytest tests/test_runner.py -q
```

Expected: FAIL because `prompt_architecture_checker.runner` does not exist yet.

- [ ] **Step 3: Implement the experimental subprocess runner**

`src/prompt_architecture_checker/config.py`

```python
import os
import shlex
import tomllib
from pathlib import Path


def resolve_copilot_command(config_path: Path | None = None) -> list[str]:
    env_command = os.environ.get("PAC_COPILOT_BIN")
    if env_command:
        return shlex.split(env_command)

    config_path = config_path or Path("prompt-architecture-checker.toml")
    if config_path.exists():
        payload = tomllib.loads(config_path.read_text(encoding="utf-8"))
        configured = payload.get("runner", {}).get("command")
        if configured:
            return shlex.split(configured)

    return ["copilot"]
```

`src/prompt_architecture_checker/runner.py`

```python
import subprocess
from pathlib import Path
from typing import Protocol, Sequence

from .config import resolve_copilot_command


class RunnerInvocationError(RuntimeError):
    pass


class SkillRunner(Protocol):
    def run(self, prompt: str) -> str: ...


class CopilotCliRunner:
    def __init__(
        self,
        command: Sequence[str] | None = None,
        config_path: Path | None = None,
    ):
        self.command = list(command) if command is not None else resolve_copilot_command(config_path)

    def run(self, prompt: str) -> str:
        completed = subprocess.run(
            self.command,
            input=prompt,
            text=True,
            capture_output=True,
            check=False,
        )

        if completed.returncode != 0:
            message = completed.stderr.strip() or "Copilot runner failed."
            raise RunnerInvocationError(message)

        return completed.stdout.strip()
```

- [ ] **Step 4: Run the runner tests to verify the experimental bridge works with a fake subprocess**

Run:

```bash
python -m pytest tests/test_runner.py -q
```

Expected: PASS with `3 passed`.

- [ ] **Step 5: Commit the runner bridge**

Run:

```bash
git add src/prompt_architecture_checker/config.py src/prompt_architecture_checker/runner.py tests/test_runner.py
git commit -m "feat: add copilot runner bridge" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds only the subprocess bridge and its tests.

### Task 4: Implement `parse <repo>` end to end

**Files:**
- Create: `src/prompt_architecture_checker/orchestrator.py`
- Create: `src/prompt_architecture_checker/output.py`
- Modify: `src/prompt_architecture_checker/cli.py`
- Create: `tests/test_cli_parse.py`
- Test: `tests/test_cli_parse.py`

- [ ] **Step 1: Write the failing parse command test**

`tests/test_cli_parse.py`

```python
import json

from prompt_architecture_checker.cli import main


def test_parse_command_prints_stage_progress_and_parse_result(
    sample_repo,
    stub_runner_factory,
    capsys,
):
    runner = stub_runner_factory(
        json.dumps(
            {
                "summary": ["ui-test-orchestrator"],
                "graph": ["ui-test-orchestrator -> report-generator"],
                "evidence": ["examples/sample-orchestrator.contract.json"],
                "uncertainties": ["failure cleanup inferred"],
            }
        )
    )

    exit_code = main(["parse", str(sample_repo)], runner=runner)
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Parsing..." in output
    assert "Parse complete:" in output
    assert "ui-test-orchestrator" in output
    assert "failure cleanup inferred" in output
    assert len(runner.prompts) == 1
    assert "Stage: parse" in runner.prompts[0]
```

- [ ] **Step 2: Run the parse test to confirm the command dispatch does not exist yet**

Run:

```bash
python -m pytest tests/test_cli_parse.py -q
```

Expected: FAIL because `main()` does not accept `runner` or print parse-stage output.

- [ ] **Step 3: Implement parse orchestration, parse rendering, and CLI dispatch**

`src/prompt_architecture_checker/orchestrator.py`

```python
import json
from pathlib import Path

from .contracts import ParseArtifact, parse_parse_artifact
from .prompt_builder import build_parse_prompt
from .runner import SkillRunner
from .skill_assets import load_skill_text


def run_parse(repo_path: Path, runner: SkillRunner) -> ParseArtifact:
    skill_text = load_skill_text("parse")
    prompt = build_parse_prompt(repo_path, skill_text)
    raw_response = runner.run(prompt)
    payload = json.loads(raw_response)
    return parse_parse_artifact(payload)
```

`src/prompt_architecture_checker/output.py`

```python
from pathlib import Path

from .contracts import ParseArtifact


def render_parse(artifact: ParseArtifact) -> str:
    lines = ["# Parse Result", "", "## Summary", ""]
    lines.extend(f"- {item}" for item in artifact.summary)
    lines.extend(["", "## Graph", ""])
    lines.extend(f"- {item}" for item in artifact.graph)
    lines.extend(["", "## Evidence", ""])
    lines.extend(f"- {item}" for item in artifact.evidence)
    lines.extend(["", "## Uncertainties", ""])
    lines.extend(f"- {item}" for item in artifact.uncertainties)
    return "\n".join(lines)


def write_output(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")
```

Replace `src/prompt_architecture_checker/cli.py` with:

```python
import argparse
import sys
from pathlib import Path
from typing import Sequence

from .orchestrator import run_parse
from .output import render_parse, write_output
from .runner import CopilotCliRunner, SkillRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-architecture-checker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("parse", "review", "report"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("repo")
        subparser.add_argument("--out", dest="out_path")

    return parser


def main(
    argv: Sequence[str] | None = None,
    runner: SkillRunner | None = None,
    stdout=None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    runner = runner or CopilotCliRunner()
    stdout = stdout or sys.stdout
    repo_path = Path(args.repo)

    if args.command == "parse":
        print("Parsing...", file=stdout)
        artifact = run_parse(repo_path, runner)
        body = render_parse(artifact)
        print(
            f"Parse complete: {len(artifact.summary)} summary items, {len(artifact.graph)} graph edges",
            file=stdout,
        )
        print(body, file=stdout)
        if args.out_path:
            write_output(Path(args.out_path), body)
        return 0

    return 0
```

- [ ] **Step 4: Run the parse test to verify the command works**

Run:

```bash
python -m pytest tests/test_cli_parse.py -q
```

Expected: PASS with `1 passed`.

- [ ] **Step 5: Commit the parse command**

Run:

```bash
git add src/prompt_architecture_checker/orchestrator.py src/prompt_architecture_checker/output.py src/prompt_architecture_checker/cli.py tests/test_cli_parse.py
git commit -m "feat: add parse command pipeline" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds only parse-stage command behavior.

### Task 5: Implement `review <repo>` orchestration

**Files:**
- Modify: `src/prompt_architecture_checker/orchestrator.py`
- Modify: `src/prompt_architecture_checker/output.py`
- Modify: `src/prompt_architecture_checker/cli.py`
- Create: `tests/test_cli_review.py`
- Test: `tests/test_cli_review.py`

- [ ] **Step 1: Write the failing review command test**

`tests/test_cli_review.py`

```python
import json

from prompt_architecture_checker.cli import main


def test_review_command_runs_parse_then_review_and_prints_findings_only(
    sample_repo,
    stub_runner_factory,
    capsys,
):
    runner = stub_runner_factory(
        json.dumps(
            {
                "summary": ["ui-test-orchestrator"],
                "graph": ["ui-test-orchestrator -> report-generator"],
                "evidence": ["examples/sample-orchestrator.contract.json"],
                "uncertainties": ["failure cleanup inferred"],
            }
        ),
        json.dumps(
            {
                "findings": [
                    {
                        "severity": "warning",
                        "findingClass": "high-risk-signal",
                        "category": "flow",
                        "artifactScope": "examples/sample-orchestrator.contract.json",
                        "message": "Release flow is not explicit on failure.",
                        "evidence": ["Completion text exists but no failure-path edge is declared."],
                        "whyItMatters": "Cleanup behavior cannot be verified from declared structure.",
                        "suggestedFix": "Add a failure-path cleanup edge.",
                    }
                ]
            }
        ),
    )

    exit_code = main(["review", str(sample_repo)], runner=runner)
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Parsing..." in output
    assert "Reviewing..." in output
    assert "Release flow is not explicit on failure." in output
    assert "# Parse Result" not in output
    assert len(runner.prompts) == 2
    assert "Stage: parse" in runner.prompts[0]
    assert "Stage: review" in runner.prompts[1]
```

- [ ] **Step 2: Run the review test to verify the command is not implemented yet**

Run:

```bash
python -m pytest tests/test_cli_review.py -q
```

Expected: FAIL because `review` still returns without running stage orchestration.

- [ ] **Step 3: Extend orchestration, rendering, and CLI dispatch for review**

Append to `src/prompt_architecture_checker/orchestrator.py`:

```python
from .contracts import ReviewArtifact, parse_review_artifact
from .prompt_builder import build_review_prompt


def run_review(repo_path: Path, runner: SkillRunner) -> tuple[ParseArtifact, ReviewArtifact]:
    parse_artifact = run_parse(repo_path, runner)
    skill_text = load_skill_text("review")
    prompt = build_review_prompt(repo_path, skill_text, parse_artifact)
    raw_response = runner.run(prompt)
    payload = json.loads(raw_response)
    review_artifact = parse_review_artifact(payload)
    return parse_artifact, review_artifact
```

Append to `src/prompt_architecture_checker/output.py`:

```python
from .contracts import ReviewArtifact


def render_review(artifact: ReviewArtifact) -> str:
    severity_order = ("error", "warning", "info")
    lines = ["## Findings", ""]

    for severity in severity_order:
        matching = [item for item in artifact.findings if item.severity == severity]
        if not matching:
            continue

        lines.append(f"### {severity.title()}")
        lines.append("")

        for index, finding in enumerate(matching, start=1):
            lines.extend(
                [
                    f"{index}. **{finding.category}** `{finding.artifact_scope}`",
                    f"   - **Class:** {finding.finding_class}",
                    f"   - **Issue:** {finding.message}",
                    f"   - **Evidence:** {'; '.join(finding.evidence)}",
                    f"   - **Why it matters:** {finding.why_it_matters}",
                    f"   - **Suggested fix:** {finding.suggested_fix}",
                ]
            )

        lines.append("")

    return "\n".join(lines).rstrip()
```

Replace `src/prompt_architecture_checker/cli.py` with:

```python
import argparse
import sys
from pathlib import Path
from typing import Sequence

from .orchestrator import run_parse, run_review
from .output import render_parse, render_review, write_output
from .runner import CopilotCliRunner, SkillRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-architecture-checker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("parse", "review", "report"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("repo")
        subparser.add_argument("--out", dest="out_path")

    return parser


def main(
    argv: Sequence[str] | None = None,
    runner: SkillRunner | None = None,
    stdout=None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    runner = runner or CopilotCliRunner()
    stdout = stdout or sys.stdout
    repo_path = Path(args.repo)

    if args.command == "parse":
        print("Parsing...", file=stdout)
        artifact = run_parse(repo_path, runner)
        body = render_parse(artifact)
        print(
            f"Parse complete: {len(artifact.summary)} summary items, {len(artifact.graph)} graph edges",
            file=stdout,
        )
        print(body, file=stdout)
        if args.out_path:
            write_output(Path(args.out_path), body)
        return 0

    if args.command == "review":
        print("Parsing...", file=stdout)
        parse_artifact, review_artifact = run_review(repo_path, runner)
        print(
            f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
            file=stdout,
        )
        print("Reviewing...", file=stdout)
        body = render_review(review_artifact)
        print(
            f"Review complete: {len(review_artifact.findings)} findings",
            file=stdout,
        )
        print(body, file=stdout)
        if args.out_path:
            write_output(Path(args.out_path), body)
        return 0

    return 0
```

- [ ] **Step 4: Run the review test to verify parse -> review orchestration**

Run:

```bash
python -m pytest tests/test_cli_review.py -q
```

Expected: PASS with `1 passed`.

- [ ] **Step 5: Commit the review command**

Run:

```bash
git add src/prompt_architecture_checker/orchestrator.py src/prompt_architecture_checker/output.py src/prompt_architecture_checker/cli.py tests/test_cli_review.py
git commit -m "feat: add review command orchestration" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds review-stage chaining and focused findings output.

### Task 6: Implement `report <repo>` orchestration and `--out`

**Files:**
- Modify: `src/prompt_architecture_checker/orchestrator.py`
- Modify: `src/prompt_architecture_checker/output.py`
- Modify: `src/prompt_architecture_checker/cli.py`
- Create: `tests/test_cli_report.py`
- Test: `tests/test_cli_report.py`
- Test: `tests/test_cli_parse.py`
- Test: `tests/test_cli_review.py`

- [ ] **Step 1: Write the failing report command test**

`tests/test_cli_report.py`

```python
import json

from prompt_architecture_checker.cli import main


def test_report_command_runs_all_stages_and_writes_primary_output(
    sample_repo,
    stub_runner_factory,
    tmp_path,
    capsys,
):
    output_path = tmp_path / "report.md"
    runner = stub_runner_factory(
        json.dumps(
            {
                "summary": ["ui-test-orchestrator"],
                "graph": ["ui-test-orchestrator -> report-generator"],
                "evidence": ["examples/sample-orchestrator.contract.json"],
                "uncertainties": ["failure cleanup inferred"],
            }
        ),
        json.dumps(
            {
                "findings": [
                    {
                        "severity": "warning",
                        "findingClass": "high-risk-signal",
                        "category": "flow",
                        "artifactScope": "examples/sample-orchestrator.contract.json",
                        "message": "Release flow is not explicit on failure.",
                        "evidence": ["Completion text exists but no failure-path edge is declared."],
                        "whyItMatters": "Cleanup behavior cannot be verified from declared structure.",
                        "suggestedFix": "Add a failure-path cleanup edge.",
                    }
                ]
            }
        ),
        "# Sample Report\n\n## Highest-Priority Findings\n\n- Release flow is not explicit on failure.\n",
    )

    exit_code = main(
        ["report", str(sample_repo), "--out", str(output_path)],
        runner=runner,
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Parsing..." in output
    assert "Reviewing..." in output
    assert "Reporting..." in output
    assert "# Sample Report" in output
    assert output_path.read_text(encoding="utf-8").startswith("# Sample Report")
    assert len(runner.prompts) == 3
    assert "Stage: parse" in runner.prompts[0]
    assert "Stage: review" in runner.prompts[1]
    assert "Stage: report" in runner.prompts[2]
```

- [ ] **Step 2: Run the report test to confirm the final stage is not implemented yet**

Run:

```bash
python -m pytest tests/test_cli_report.py -q
```

Expected: FAIL because `report` still returns before running all three stages.

- [ ] **Step 3: Extend orchestration and CLI dispatch for report output**

Append to `src/prompt_architecture_checker/orchestrator.py`:

```python
from .contracts import ReportArtifact
from .prompt_builder import build_report_prompt


def run_report(
    repo_path: Path,
    runner: SkillRunner,
) -> tuple[ParseArtifact, ReviewArtifact, ReportArtifact]:
    parse_artifact, review_artifact = run_review(repo_path, runner)
    skill_text = load_skill_text("report")
    prompt = build_report_prompt(
        repo_path,
        skill_text,
        parse_artifact,
        review_artifact,
    )
    raw_response = runner.run(prompt)
    return parse_artifact, review_artifact, ReportArtifact(markdown=raw_response)
```

Append to `src/prompt_architecture_checker/output.py`:

```python
from .contracts import ReportArtifact


def render_report(artifact: ReportArtifact) -> str:
    return artifact.markdown
```

Replace `src/prompt_architecture_checker/cli.py` with:

```python
import argparse
import sys
from pathlib import Path
from typing import Sequence

from .orchestrator import run_parse, run_report, run_review
from .output import render_parse, render_report, render_review, write_output
from .runner import CopilotCliRunner, SkillRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-architecture-checker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("parse", "review", "report"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("repo")
        subparser.add_argument("--out", dest="out_path")

    return parser


def main(
    argv: Sequence[str] | None = None,
    runner: SkillRunner | None = None,
    stdout=None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    runner = runner or CopilotCliRunner()
    stdout = stdout or sys.stdout
    repo_path = Path(args.repo)

    if args.command == "parse":
        print("Parsing...", file=stdout)
        artifact = run_parse(repo_path, runner)
        body = render_parse(artifact)
        print(
            f"Parse complete: {len(artifact.summary)} summary items, {len(artifact.graph)} graph edges",
            file=stdout,
        )
        print(body, file=stdout)
        if args.out_path:
            write_output(Path(args.out_path), body)
        return 0

    if args.command == "review":
        print("Parsing...", file=stdout)
        parse_artifact, review_artifact = run_review(repo_path, runner)
        print(
            f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
            file=stdout,
        )
        print("Reviewing...", file=stdout)
        body = render_review(review_artifact)
        print(
            f"Review complete: {len(review_artifact.findings)} findings",
            file=stdout,
        )
        print(body, file=stdout)
        if args.out_path:
            write_output(Path(args.out_path), body)
        return 0

    print("Parsing...", file=stdout)
    parse_artifact, review_artifact, report_artifact = run_report(repo_path, runner)
    print(
        f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
        file=stdout,
    )
    print("Reviewing...", file=stdout)
    print(
        f"Review complete: {len(review_artifact.findings)} findings",
        file=stdout,
    )
    print("Reporting...", file=stdout)
    body = render_report(report_artifact)
    print("Report complete: markdown ready", file=stdout)
    print(body, file=stdout)
    if args.out_path:
        write_output(Path(args.out_path), body)
    return 0
```

- [ ] **Step 4: Run the report test to verify full stage chaining and `--out`**

Run:

```bash
python -m pytest tests/test_cli_report.py -q
```

Expected: PASS with `1 passed`.

- [ ] **Step 5: Run the command test suite to verify no regressions across the three entrypoints**

Run:

```bash
python -m pytest tests/test_cli_parse.py tests/test_cli_review.py tests/test_cli_report.py -q
```

Expected: PASS with `3 passed`.

- [ ] **Step 6: Commit the report command**

Run:

```bash
git add src/prompt_architecture_checker/orchestrator.py src/prompt_architecture_checker/output.py src/prompt_architecture_checker/cli.py tests/test_cli_report.py
git commit -m "feat: add report command pipeline" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that completes the staged parse -> review -> report command flow.

### Task 7: Add repo validation and clear stage failure handling

**Files:**
- Modify: `src/prompt_architecture_checker/orchestrator.py`
- Modify: `src/prompt_architecture_checker/cli.py`
- Create: `tests/test_cli_errors.py`
- Test: `tests/test_cli_errors.py`
- Test: `tests/test_cli_parse.py`
- Test: `tests/test_cli_review.py`
- Test: `tests/test_cli_report.py`

- [ ] **Step 1: Write the failing CLI error-handling tests**

`tests/test_cli_errors.py`

```python
from prompt_architecture_checker.cli import main
from prompt_architecture_checker.runner import RunnerInvocationError


class ExplodingRunner:
    def run(self, prompt: str) -> str:
        raise RunnerInvocationError("runner failed")


def test_parse_command_rejects_missing_repo(tmp_path, capsys):
    missing_repo = tmp_path / "missing"

    exit_code = main(["parse", str(missing_repo)])
    error_output = capsys.readouterr().err

    assert exit_code == 2
    assert "Repository path does not exist" in error_output


def test_review_command_surfaces_stage_failure(sample_repo, capsys):
    exit_code = main(["review", str(sample_repo)], runner=ExplodingRunner())
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "parse stage failed: runner failed" in error_output
```

- [ ] **Step 2: Run the error test to confirm validation and stage failures are not surfaced yet**

Run:

```bash
python -m pytest tests/test_cli_errors.py -q
```

Expected: FAIL because `main()` does not validate repo paths or convert runner failures into stage-specific CLI errors.

- [ ] **Step 3: Add explicit stage errors in the orchestrator and validate repo paths in the CLI**

Append to `src/prompt_architecture_checker/orchestrator.py`:

```python
class StageExecutionError(RuntimeError):
    def __init__(self, stage: str, message: str):
        super().__init__(message)
        self.stage = stage
```

Replace `src/prompt_architecture_checker/orchestrator.py` with:

```python
import json
from pathlib import Path

from .contracts import (
    ParseArtifact,
    ReportArtifact,
    ReviewArtifact,
    parse_parse_artifact,
    parse_review_artifact,
)
from .prompt_builder import build_parse_prompt, build_report_prompt, build_review_prompt
from .runner import RunnerInvocationError, SkillRunner
from .skill_assets import load_skill_text


class StageExecutionError(RuntimeError):
    def __init__(self, stage: str, message: str):
        super().__init__(message)
        self.stage = stage


def run_parse(repo_path: Path, runner: SkillRunner) -> ParseArtifact:
    try:
        skill_text = load_skill_text("parse")
        prompt = build_parse_prompt(repo_path, skill_text)
        raw_response = runner.run(prompt)
        payload = json.loads(raw_response)
        return parse_parse_artifact(payload)
    except (RunnerInvocationError, json.JSONDecodeError, KeyError) as exc:
        raise StageExecutionError("parse", str(exc)) from exc


def run_review(repo_path: Path, runner: SkillRunner) -> tuple[ParseArtifact, ReviewArtifact]:
    parse_artifact = run_parse(repo_path, runner)

    try:
        skill_text = load_skill_text("review")
        prompt = build_review_prompt(repo_path, skill_text, parse_artifact)
        raw_response = runner.run(prompt)
        payload = json.loads(raw_response)
        review_artifact = parse_review_artifact(payload)
        return parse_artifact, review_artifact
    except (RunnerInvocationError, json.JSONDecodeError, KeyError) as exc:
        raise StageExecutionError("review", str(exc)) from exc


def run_report(
    repo_path: Path,
    runner: SkillRunner,
) -> tuple[ParseArtifact, ReviewArtifact, ReportArtifact]:
    parse_artifact, review_artifact = run_review(repo_path, runner)

    try:
        skill_text = load_skill_text("report")
        prompt = build_report_prompt(
            repo_path,
            skill_text,
            parse_artifact,
            review_artifact,
        )
        raw_response = runner.run(prompt)
        return parse_artifact, review_artifact, ReportArtifact(markdown=raw_response)
    except RunnerInvocationError as exc:
        raise StageExecutionError("report", str(exc)) from exc
```

Replace `src/prompt_architecture_checker/cli.py` with:

```python
import argparse
import sys
from pathlib import Path
from typing import Sequence

from .orchestrator import StageExecutionError, run_parse, run_report, run_review
from .output import render_parse, render_report, render_review, write_output
from .runner import CopilotCliRunner, SkillRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-architecture-checker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("parse", "review", "report"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("repo")
        subparser.add_argument("--out", dest="out_path")

    return parser


def _validate_repo_path(repo_path: Path) -> str | None:
    if not repo_path.exists():
        return f"Repository path does not exist: {repo_path}"
    if not repo_path.is_dir():
        return f"Repository path is not a directory: {repo_path}"
    return None


def main(
    argv: Sequence[str] | None = None,
    runner: SkillRunner | None = None,
    stdout=None,
    stderr=None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    runner = runner or CopilotCliRunner()
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    repo_path = Path(args.repo)

    validation_error = _validate_repo_path(repo_path)
    if validation_error is not None:
        print(validation_error, file=stderr)
        return 2

    try:
        if args.command == "parse":
            print("Parsing...", file=stdout)
            artifact = run_parse(repo_path, runner)
            body = render_parse(artifact)
            print(
                f"Parse complete: {len(artifact.summary)} summary items, {len(artifact.graph)} graph edges",
                file=stdout,
            )
            print(body, file=stdout)
            if args.out_path:
                write_output(Path(args.out_path), body)
            return 0

        if args.command == "review":
            print("Parsing...", file=stdout)
            parse_artifact, review_artifact = run_review(repo_path, runner)
            print(
                f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
                file=stdout,
            )
            print("Reviewing...", file=stdout)
            body = render_review(review_artifact)
            print(
                f"Review complete: {len(review_artifact.findings)} findings",
                file=stdout,
            )
            print(body, file=stdout)
            if args.out_path:
                write_output(Path(args.out_path), body)
            return 0

        print("Parsing...", file=stdout)
        parse_artifact, review_artifact, report_artifact = run_report(repo_path, runner)
        print(
            f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
            file=stdout,
        )
        print("Reviewing...", file=stdout)
        print(
            f"Review complete: {len(review_artifact.findings)} findings",
            file=stdout,
        )
        print("Reporting...", file=stdout)
        body = render_report(report_artifact)
        print("Report complete: markdown ready", file=stdout)
        print(body, file=stdout)
        if args.out_path:
            write_output(Path(args.out_path), body)
        return 0
    except StageExecutionError as exc:
        print(f"{exc.stage} stage failed: {exc}", file=stderr)
        return 1
```

- [ ] **Step 4: Run the error-handling test to verify clear setup and stage failures**

Run:

```bash
python -m pytest tests/test_cli_errors.py -q
```

Expected: PASS with `2 passed`.

- [ ] **Step 5: Run the full CLI test suite to verify the error handling did not break the happy paths**

Run:

```bash
python -m pytest tests/test_cli_parse.py tests/test_cli_review.py tests/test_cli_report.py tests/test_cli_errors.py -q
```

Expected: PASS with `5 passed`.

- [ ] **Step 6: Commit the validation and error handling**

Run:

```bash
git add src/prompt_architecture_checker/orchestrator.py src/prompt_architecture_checker/cli.py tests/test_cli_errors.py
git commit -m "feat: add cli validation and stage errors" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that adds repo validation and stage-specific failure reporting.

### Task 8: Document installation, command usage, and experimental bridge behavior

**Files:**
- Modify: `README.md`
- Test: `README.md`

- [ ] **Step 1: Prove the README does not yet document the Python CLI usage**

Run:

```bash
rg "^## Experimental CLI$|^prompt-architecture-checker parse \\.$|^prompt-architecture-checker review \\.$|^prompt-architecture-checker report \\. --out report.md$" README.md -n
```

Expected: no matches.

- [ ] **Step 2: Add an `## Experimental CLI` section to the README**

Insert this block after `## Suggested Product Path`:

````md
## Experimental CLI

The repository now includes an experimental Python CLI that shells out to the local `copilot` executable as a stage runner.

Install the package locally:

```bash
python -m pip install -e .[dev]
```

Run the three first-slice commands:

```bash
prompt-architecture-checker parse .
prompt-architecture-checker review .
prompt-architecture-checker report . --out report.md
```

The first implementation uses an experimental Copilot subprocess bridge. It expects `copilot` to be available on `PATH`, or for `PAC_COPILOT_BIN` to point at the executable to launch.

To override the runner command without using an environment variable, create `prompt-architecture-checker.toml` with:

```toml
[runner]
command = "copilot --experimental"
```
````

- [ ] **Step 3: Verify the README now documents the CLI entrypoints**

Run:

```bash
rg "^## Experimental CLI$|^prompt-architecture-checker parse \\.$|^prompt-architecture-checker review \\.$|^prompt-architecture-checker report \\. --out report.md$|^The first implementation uses an experimental Copilot subprocess bridge\\.$|^command = \"copilot --experimental\"$" README.md -n
```

Expected: 6 matches.

- [ ] **Step 4: Commit the README update**

Run:

```bash
git add README.md
git commit -m "docs: add experimental cli usage" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected: a commit that changes only `README.md`.
