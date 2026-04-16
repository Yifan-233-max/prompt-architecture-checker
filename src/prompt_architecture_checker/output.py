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
