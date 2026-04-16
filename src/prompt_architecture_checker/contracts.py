from dataclasses import dataclass
from typing import Any

SUPPORTED_REVIEW_SEVERITIES = {"error", "warning", "info"}


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
    findings = []
    for item in payload["findings"]:
        severity = item["severity"]
        if severity not in SUPPORTED_REVIEW_SEVERITIES:
            supported = ", ".join(sorted(SUPPORTED_REVIEW_SEVERITIES))
            raise ValueError(
                f"Unsupported review finding severity '{severity}'. "
                f"Supported severities: {supported}."
            )

        findings.append(
            ReviewFinding(
                severity=severity,
                finding_class=item["findingClass"],
                category=item["category"],
                artifact_scope=item["artifactScope"],
                message=item["message"],
                evidence=list(item["evidence"]),
                why_it_matters=item["whyItMatters"],
                suggested_fix=item["suggestedFix"],
            )
        )

    return ReviewArtifact(
        findings=findings
    )
