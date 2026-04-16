from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILL_PATHS = {
    "parse": ROOT / "skills" / "parse-skill" / "SKILL.md",
    "review": ROOT / "skills" / "review-skill" / "SKILL.md",
    "report": ROOT / "skills" / "report-skill" / "SKILL.md",
}


def load_skill_text(stage: str) -> str:
    skill_path = SKILL_PATHS.get(stage)
    if skill_path is None:
        supported_stages = ", ".join(sorted(SKILL_PATHS))
        raise ValueError(
            f"Unknown skill stage '{stage}'. Expected one of: {supported_stages}."
        )

    try:
        return skill_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Missing skill asset for '{stage}' stage at '{skill_path}'. "
            "This experimental CLI expects repository skill assets to be available "
            "from an editable install in a repository checkout."
        ) from exc
