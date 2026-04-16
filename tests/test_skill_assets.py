from pathlib import Path

import pytest

from prompt_architecture_checker.contracts import (
    parse_parse_artifact,
    parse_review_artifact,
)
from prompt_architecture_checker.prompt_builder import build_review_prompt
from prompt_architecture_checker.skill_assets import load_skill_text


def test_load_skill_text_returns_parse_skill_content():
    text = load_skill_text("parse")

    assert "Return JSON only" in text
    assert "summary" in text


def test_parse_artifact_parser_reads_expected_shape():
    artifact = parse_parse_artifact(
        {
            "summary": ["ui-test-orchestrator"],
            "graph": ["ui-test-orchestrator -> report-generator"],
            "evidence": ["examples/sample-orchestrator.contract.json"],
            "uncertainties": ["failure cleanup inferred"],
        }
    )

    assert artifact.summary == ["ui-test-orchestrator"]
    assert artifact.graph == ["ui-test-orchestrator -> report-generator"]


def test_review_artifact_parser_reads_expected_shape():
    artifact = parse_review_artifact(
        {
            "findings": [
                {
                    "severity": "warning",
                    "findingClass": "high-risk-signal",
                    "category": "flow",
                    "artifactScope": "examples/sample-orchestrator.contract.json",
                    "message": "Release flow is not explicit on failure.",
                    "evidence": [
                        "Completion text exists but no failure-path edge is declared."
                    ],
                    "whyItMatters": "Cleanup behavior cannot be verified from declared structure.",
                    "suggestedFix": "Add a failure-path cleanup edge.",
                }
            ]
        }
    )

    assert artifact.findings[0].severity == "warning"
    assert artifact.findings[0].category == "flow"


def test_review_artifact_parser_rejects_unsupported_severity():
    with pytest.raises(ValueError) as excinfo:
        parse_review_artifact(
            {
                "findings": [
                    {
                        "severity": "critical",
                        "findingClass": "high-risk-signal",
                        "category": "flow",
                        "artifactScope": "examples/sample-orchestrator.contract.json",
                        "message": "Release flow is not explicit on failure.",
                        "evidence": [
                            "Completion text exists but no failure-path edge is declared."
                        ],
                        "whyItMatters": "Cleanup behavior cannot be verified from declared structure.",
                        "suggestedFix": "Add a failure-path cleanup edge.",
                    }
                ]
            }
        )

    assert "Unsupported review finding severity" in str(excinfo.value)
    assert "critical" in str(excinfo.value)


def test_build_review_prompt_embeds_parse_artifact():
    parse_artifact = parse_parse_artifact(
        {
            "summary": ["ui-test-orchestrator"],
            "graph": ["ui-test-orchestrator -> report-generator"],
            "evidence": ["examples/sample-orchestrator.contract.json"],
            "uncertainties": ["failure cleanup inferred"],
        }
    )

    prompt = build_review_prompt(
        Path("repo"),
        load_skill_text("review"),
        parse_artifact,
    )

    assert "Stage: review" in prompt
    assert '"summary": [' in prompt
