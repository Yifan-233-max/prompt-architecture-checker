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
