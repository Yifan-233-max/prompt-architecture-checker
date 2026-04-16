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
    except FileNotFoundError as exc:
        raise StageExecutionError("parse", str(exc)) from exc

    try:
        prompt = build_parse_prompt(repo_path, skill_text)
        raw_response = runner.run(prompt)
        payload = json.loads(raw_response)
        return parse_parse_artifact(payload)
    except (RunnerInvocationError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise StageExecutionError("parse", str(exc)) from exc


def run_review_stage(
    repo_path: Path,
    runner: SkillRunner,
    parse_artifact: ParseArtifact,
) -> ReviewArtifact:
    try:
        skill_text = load_skill_text("review")
    except FileNotFoundError as exc:
        raise StageExecutionError("review", str(exc)) from exc

    try:
        prompt = build_review_prompt(repo_path, skill_text, parse_artifact)
        raw_response = runner.run(prompt)
        payload = json.loads(raw_response)
        return parse_review_artifact(payload)
    except (RunnerInvocationError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise StageExecutionError("review", str(exc)) from exc


def run_review(repo_path: Path, runner: SkillRunner) -> tuple[ParseArtifact, ReviewArtifact]:
    parse_artifact = run_parse(repo_path, runner)
    review_artifact = run_review_stage(repo_path, runner, parse_artifact)
    return parse_artifact, review_artifact


def run_report_stage(
    repo_path: Path,
    runner: SkillRunner,
    parse_artifact: ParseArtifact,
    review_artifact: ReviewArtifact,
) -> ReportArtifact:
    try:
        skill_text = load_skill_text("report")
    except FileNotFoundError as exc:
        raise StageExecutionError("report", str(exc)) from exc

    try:
        prompt = build_report_prompt(
            repo_path,
            skill_text,
            parse_artifact,
            review_artifact,
        )
        raw_response = runner.run(prompt)
        return ReportArtifact(markdown=raw_response)
    except RunnerInvocationError as exc:
        raise StageExecutionError("report", str(exc)) from exc


def run_report(
    repo_path: Path,
    runner: SkillRunner,
) -> tuple[ParseArtifact, ReviewArtifact, ReportArtifact]:
    parse_artifact, review_artifact = run_review(repo_path, runner)
    report_artifact = run_report_stage(repo_path, runner, parse_artifact, review_artifact)
    return parse_artifact, review_artifact, report_artifact
