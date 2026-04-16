import json

from prompt_architecture_checker.orchestrator import run_report, run_review


def test_run_review_returns_parse_and_review_artifacts(sample_repo, stub_runner_factory):
    runner = stub_runner_factory(
        json.dumps(
            {
                "summary": ["ui-test-orchestrator"],
                "graph": ["ui-test-orchestrator -> report-generator"],
                "evidence": ["examples/sample-orchestrator.contract.json"],
                "uncertainties": ["failure cleanup inferred"],
            }
        ),
        json.dumps(
            {
                "findings": [
                    {
                        "severity": "warning",
                        "findingClass": "high-risk-signal",
                        "category": "flow",
                        "artifactScope": "examples/sample-orchestrator.contract.json",
                        "message": "Release flow is not explicit on failure.",
                        "evidence": ["Completion text exists but no failure-path edge is declared."],
                        "whyItMatters": "Cleanup behavior cannot be verified from declared structure.",
                        "suggestedFix": "Add a failure-path cleanup edge.",
                    }
                ]
            }
        ),
    )

    parse_artifact, review_artifact = run_review(sample_repo, runner)

    assert parse_artifact.summary == ["ui-test-orchestrator"]
    assert review_artifact.findings[0].severity == "warning"


def test_run_report_returns_parse_review_and_report_artifacts(
    sample_repo,
    stub_runner_factory,
):
    runner = stub_runner_factory(
        json.dumps(
            {
                "summary": ["ui-test-orchestrator"],
                "graph": ["ui-test-orchestrator -> report-generator"],
                "evidence": ["examples/sample-orchestrator.contract.json"],
                "uncertainties": ["failure cleanup inferred"],
            }
        ),
        json.dumps(
            {
                "findings": [
                    {
                        "severity": "warning",
                        "findingClass": "high-risk-signal",
                        "category": "flow",
                        "artifactScope": "examples/sample-orchestrator.contract.json",
                        "message": "Release flow is not explicit on failure.",
                        "evidence": ["Completion text exists but no failure-path edge is declared."],
                        "whyItMatters": "Cleanup behavior cannot be verified from declared structure.",
                        "suggestedFix": "Add a failure-path cleanup edge.",
                    }
                ]
            }
        ),
        "# Sample Report\n",
    )

    parse_artifact, review_artifact, report_artifact = run_report(sample_repo, runner)

    assert parse_artifact.summary == ["ui-test-orchestrator"]
    assert review_artifact.findings[0].severity == "warning"
    assert report_artifact.markdown == "# Sample Report\n"
