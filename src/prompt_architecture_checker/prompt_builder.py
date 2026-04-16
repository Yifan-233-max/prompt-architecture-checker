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
