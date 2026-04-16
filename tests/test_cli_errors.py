from prompt_architecture_checker.cli import main
from prompt_architecture_checker.runner import RunnerInvocationError


class ExplodingRunner:
    def run(self, prompt: str) -> str:
        raise RunnerInvocationError("runner failed")


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
