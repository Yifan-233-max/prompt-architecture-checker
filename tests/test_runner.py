import sys

import pytest

from prompt_architecture_checker.config import resolve_copilot_command
from prompt_architecture_checker.runner import CopilotCliRunner, RunnerInvocationError


def test_resolve_copilot_command_prefers_env_over_config(tmp_path, monkeypatch):
    config_path = tmp_path / "prompt-architecture-checker.toml"
    config_path.write_text('[runner]\ncommand = "copilot --experimental"\n', encoding="utf-8")
    monkeypatch.setenv("PAC_COPILOT_BIN", "copilot-preview")

    assert resolve_copilot_command(config_path) == ["copilot-preview"]


def test_copilot_runner_returns_stdout_from_subprocess(tmp_path):
    script = tmp_path / "fake_copilot.py"
    script.write_text(
        "import sys\n"
        "# args: [..., '-p', prompt]\n"
        "prompt = sys.argv[-1]\n"
        "sys.stdout.write(prompt.upper())\n",
        encoding="utf-8",
    )

    runner = CopilotCliRunner(command=[sys.executable, str(script)])

    assert runner.run("Stage: parse") == "STAGE: PARSE"


def test_copilot_runner_decodes_utf8_subprocess_output(tmp_path):
    script = tmp_path / "utf8_copilot.py"
    script.write_text(
        "import sys\n"
        "sys.stdout.buffer.write('✓ parse complete'.encode('utf-8'))\n",
        encoding="utf-8",
    )

    runner = CopilotCliRunner(command=[sys.executable, str(script)])

    assert runner.run('Stage: parse') == "✓ parse complete"


def test_copilot_runner_raises_on_nonzero_exit(tmp_path):
    script = tmp_path / "failing_copilot.py"
    script.write_text(
        "import sys\n"
        "sys.stderr.write('runner failed')\n"
        "raise SystemExit(2)\n",
        encoding="utf-8",
    )

    runner = CopilotCliRunner(command=[sys.executable, str(script)])

    with pytest.raises(RunnerInvocationError, match="runner failed"):
        runner.run("Stage: parse")
