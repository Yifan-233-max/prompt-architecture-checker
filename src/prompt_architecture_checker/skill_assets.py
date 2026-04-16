from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_PATHS = {
    "parse": ROOT / "skills" / "parse-skill" / "SKILL.md",
    "review": ROOT / "skills" / "review-skill" / "SKILL.md",
    "report": ROOT / "skills" / "report-skill" / "SKILL.md",
}


def load_skill_text(stage: str) -> str:
    return SKILL_PATHS[stage].read_text(encoding="utf-8")
