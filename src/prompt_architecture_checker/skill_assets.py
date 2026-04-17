from importlib.resources import files
from importlib.resources.abc import Traversable


SKILL_ASSET_DIRS = {
    "parse": "parse-skill",
    "review": "review-skill",
    "report": "report-skill",
}


def _skill_resource(stage: str) -> Traversable:
    asset_dir = SKILL_ASSET_DIRS.get(stage)
    if asset_dir is None:
        supported_stages = ", ".join(sorted(SKILL_ASSET_DIRS))
        raise ValueError(
            f"Unknown skill stage '{stage}'. Expected one of: {supported_stages}."
        )

    return (
        files("prompt_architecture_checker")
        .joinpath("assets")
        .joinpath("skills")
        .joinpath(asset_dir)
        .joinpath("SKILL.md")
    )


def load_skill_text(stage: str) -> str:
    resource = _skill_resource(stage)
    try:
        return resource.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError) as exc:
        raise FileNotFoundError(
            f"Missing bundled skill asset for '{stage}' stage. "
            "The installed prompt-architecture-checker package appears to be "
            "missing its assets/skills/ resources."
        ) from exc
