from pathlib import Path

from .contracts import ParseArtifact, ReviewArtifact


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


def write_output(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")
