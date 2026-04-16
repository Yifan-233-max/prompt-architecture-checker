import json

from prompt_architecture_checker.cli import main


def test_report_command_runs_all_stages_and_writes_primary_output(
    sample_repo,
    stub_runner_factory,
    tmp_path,
    capsys,
):
    output_path = tmp_path / "report.md"
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
        "# Sample Report\n\n## Highest-Priority Findings\n\n- Release flow is not explicit on failure.\n",
    )

    exit_code = main(
        ["report", str(sample_repo), "--out", str(output_path)],
        runner=runner,
    )
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Parsing..." in output
    assert "Reviewing..." in output
    assert "Reporting..." in output
    assert "# Sample Report" in output
    assert output_path.read_text(encoding="utf-8").startswith("# Sample Report")
    assert len(runner.prompts) == 3
    assert "Stage: parse" in runner.prompts[0]
    assert "Stage: review" in runner.prompts[1]
    assert "Stage: report" in runner.prompts[2]
