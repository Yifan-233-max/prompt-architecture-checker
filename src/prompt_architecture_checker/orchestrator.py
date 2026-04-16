import json
from pathlib import Path

from .contracts import (
    ParseArtifact,
    ReviewArtifact,
    parse_parse_artifact,
    parse_review_artifact,
)
from .prompt_builder import build_parse_prompt, build_review_prompt
from .runner import SkillRunner
from .skill_assets import load_skill_text


def run_parse(repo_path: Path, runner: SkillRunner) -> ParseArtifact:
    skill_text = load_skill_text("parse")
    prompt = build_parse_prompt(repo_path, skill_text)
    raw_response = runner.run(prompt)
    payload = json.loads(raw_response)
    return parse_parse_artifact(payload)


def run_review_stage(
    repo_path: Path,
    runner: SkillRunner,
    parse_artifact: ParseArtifact,
) -> ReviewArtifact:
    skill_text = load_skill_text("review")
    prompt = build_review_prompt(repo_path, skill_text, parse_artifact)
    raw_response = runner.run(prompt)
    payload = json.loads(raw_response)
    return parse_review_artifact(payload)


def run_review(repo_path: Path, runner: SkillRunner) -> tuple[ParseArtifact, ReviewArtifact]:
    parse_artifact = run_parse(repo_path, runner)
    review_artifact = run_review_stage(repo_path, runner, parse_artifact)
    return parse_artifact, review_artifact
