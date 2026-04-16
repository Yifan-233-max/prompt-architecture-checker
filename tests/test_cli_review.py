import json
from io import StringIO

from prompt_architecture_checker.cli import main


def test_review_command_runs_parse_then_review_and_prints_findings_only(
    sample_repo,
    stub_runner_factory,
    capsys,
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
    )

    exit_code = main(["review", str(sample_repo)], runner=runner)
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Parsing..." in output
    assert "Reviewing..." in output
    assert "Release flow is not explicit on failure." in output
    assert "# Parse Result" not in output
    assert len(runner.prompts) == 2
    assert "Stage: parse" in runner.prompts[0]
    assert "Stage: review" in runner.prompts[1]


def test_review_command_writes_primary_output_to_out_file(
    sample_repo,
    stub_runner_factory,
    tmp_path,
):
    output_path = tmp_path / "review.md"
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

    exit_code = main(
        ["review", str(sample_repo), "--out", str(output_path)],
        runner=runner,
    )

    assert exit_code == 0
    output_text = output_path.read_text(encoding="utf-8")
    assert "Release flow is not explicit on failure." in output_text
    assert "## Findings" in output_text


def test_review_command_prints_reviewing_before_review_stage_starts(
    sample_repo,
    stub_runner_factory,
):
    stdout = StringIO()
    base_runner = stub_runner_factory(
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

    class AssertingRunner:
        def __init__(self):
            self.calls = 0

        def run(self, prompt: str) -> str:
            self.calls += 1
            if self.calls == 2:
                output = stdout.getvalue()
                assert "Parsing..." in output
                assert "Reviewing..." in output
            return base_runner.run(prompt)

    exit_code = main(["review", str(sample_repo)], runner=AssertingRunner(), stdout=stdout)

    assert exit_code == 0
