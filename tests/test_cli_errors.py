import json

from prompt_architecture_checker.cli import main
from prompt_architecture_checker.runner import RunnerInvocationError
from prompt_architecture_checker import skill_assets


class ExplodingRunner:
    def run(self, prompt: str) -> str:
        raise RunnerInvocationError("runner failed")


class QueuedRunner:
    def __init__(self, *responses):
        self.responses = list(responses)

    def run(self, prompt: str) -> str:
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_parse_command_rejects_missing_repo(tmp_path, capsys):
    missing_repo = tmp_path / "missing"

    exit_code = main(["parse", str(missing_repo)])
    error_output = capsys.readouterr().err

    assert exit_code == 2
    assert "Repository path does not exist" in error_output


def test_review_command_surfaces_stage_failure(sample_repo, capsys):
    exit_code = main(["review", str(sample_repo)], runner=ExplodingRunner())
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "parse stage failed: runner failed" in error_output


def test_parse_command_surfaces_missing_skill_file(sample_repo, monkeypatch, capsys):
    monkeypatch.setitem(
        skill_assets.SKILL_PATHS,
        "parse",
        sample_repo / "missing-skill.md",
    )

    exit_code = main(["parse", str(sample_repo)], runner=QueuedRunner("unused"))
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "parse stage failed:" in error_output
    assert "missing-skill.md" in error_output
    assert "editable install" in error_output
    assert "repository checkout" in error_output
    assert "Traceback" not in error_output


def test_parse_command_surfaces_malformed_parse_payload_types(sample_repo, capsys):
    runner = QueuedRunner(
        json.dumps(
            {
                "summary": 42,
                "graph": ["ui-test-orchestrator -> report-generator"],
                "evidence": ["examples/sample-orchestrator.contract.json"],
                "uncertainties": ["failure cleanup inferred"],
            }
        )
    )

    exit_code = main(["parse", str(sample_repo)], runner=runner)
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "parse stage failed:" in error_output
    assert "Traceback" not in error_output


def test_review_command_surfaces_review_stage_failure(sample_repo, capsys):
    runner = QueuedRunner(
        json.dumps(
            {
                "summary": ["ui-test-orchestrator"],
                "graph": ["ui-test-orchestrator -> report-generator"],
                "evidence": ["examples/sample-orchestrator.contract.json"],
                "uncertainties": ["failure cleanup inferred"],
            }
        ),
        RunnerInvocationError("runner failed"),
    )

    exit_code = main(["review", str(sample_repo)], runner=runner)
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "review stage failed: runner failed" in error_output


def test_review_command_surfaces_malformed_review_payload_types(sample_repo, capsys):
    runner = QueuedRunner(
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
                "findings": {
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
            }
        ),
    )

    exit_code = main(["review", str(sample_repo)], runner=runner)
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "review stage failed:" in error_output
    assert "Traceback" not in error_output


def test_report_command_surfaces_report_stage_failure(sample_repo, capsys):
    runner = QueuedRunner(
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
        RunnerInvocationError("runner failed"),
    )

    exit_code = main(["report", str(sample_repo)], runner=runner)
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "report stage failed: runner failed" in error_output


def test_review_command_rejects_unsupported_finding_severity(sample_repo, capsys):
    runner = QueuedRunner(
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
                        "severity": "critical",
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

    exit_code = main(["review", str(sample_repo)], runner=runner)
    error_output = capsys.readouterr().err

    assert exit_code == 1
    assert "review stage failed:" in error_output
    assert "Unsupported review finding severity" in error_output
    assert "critical" in error_output
