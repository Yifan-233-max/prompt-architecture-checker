import json

from prompt_architecture_checker.cli import main


def test_parse_command_prints_stage_progress_and_parse_result(
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
        )
    )

    exit_code = main(["parse", str(sample_repo)], runner=runner)
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Parsing..." in output
    assert "Parse complete:" in output
    assert "ui-test-orchestrator" in output
    assert "failure cleanup inferred" in output
    assert len(runner.prompts) == 1
    assert "Stage: parse" in runner.prompts[0]


def test_parse_command_writes_primary_output_to_out_file(
    sample_repo,
    stub_runner_factory,
    tmp_path,
):
    output_path = tmp_path / "parse.md"
    runner = stub_runner_factory(
        json.dumps(
            {
                "summary": ["ui-test-orchestrator"],
                "graph": ["ui-test-orchestrator -> report-generator"],
                "evidence": ["examples/sample-orchestrator.contract.json"],
                "uncertainties": ["failure cleanup inferred"],
            }
        )
    )

    exit_code = main(
        ["parse", str(sample_repo), "--out", str(output_path)],
        runner=runner,
    )

    assert exit_code == 0
    output_text = output_path.read_text(encoding="utf-8")
    assert "# Parse Result" in output_text
    assert "ui-test-orchestrator" in output_text
