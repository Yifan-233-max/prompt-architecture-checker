import subprocess
from pathlib import Path
from typing import Protocol, Sequence

from .config import resolve_copilot_command


class RunnerInvocationError(RuntimeError):
    pass


class SkillRunner(Protocol):
    def run(self, prompt: str) -> str: ...


class CopilotCliRunner:
    def __init__(
        self,
        command: Sequence[str] | None = None,
        config_path: Path | None = None,
    ):
        self.command = list(command) if command is not None else resolve_copilot_command(config_path)

    def run(self, prompt: str) -> str:
        completed = subprocess.run(
            self.command,
            input=prompt,
            text=True,
            capture_output=True,
            check=False,
        )

        if completed.returncode != 0:
            message = completed.stderr.strip() or "Copilot runner failed."
            raise RunnerInvocationError(message)

        return completed.stdout.strip()
