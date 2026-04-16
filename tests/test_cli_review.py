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


def test_review_command_prints_reviewing_before_review_stage_runs(sample_repo, stub_runner_factory):
    stdout = StringIO()

    class AssertingRunner:
        def __init__(self):
            self._runner = stub_runner_factory(
                json.dumps(
                    {
                        "summary": ["ui-test-orchestrator"],
                        "graph": ["ui-test-orchestrator -> report-generator"],
                        "evidence": ["examples/sample-orchestrator.contract.json"],
                        "uncertainties": ["failure cleanup inferred"],
                    }
                ),
                json.dumps({"findings": []}),
            )

        @property
        def prompts(self):
            return self._runner.prompts

        def run(self, prompt: str) -> str:
            if len(self._runner.prompts) == 1:
                assert "Reviewing..." in stdout.getvalue()
            return self._runner.run(prompt)

    exit_code = main(["review", str(sample_repo)], runner=AssertingRunner(), stdout=stdout)

    assert exit_code == 0


def test_report_command_remains_unimplemented(sample_repo, capsys):
    exit_code = main(["report", str(sample_repo)])
    output = capsys.readouterr().out

    assert exit_code == 1
    assert "Command 'report' is not yet implemented." in output
