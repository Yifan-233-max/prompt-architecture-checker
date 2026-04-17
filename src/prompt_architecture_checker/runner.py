import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Protocol, Sequence

from .config import resolve_copilot_command


class RunnerInvocationError(RuntimeError):
    pass


class SkillRunner(Protocol):
    def run(self, prompt: str) -> str: ...


DEFAULT_COPILOT_ARGS = ("--allow-all-tools", "--no-color", "-s")


def _resolve_executable(command: Sequence[str]) -> list[str]:
    if not command:
        raise RunnerInvocationError("Empty runner command.")

    head, *tail = command
    resolved = shutil.which(head)
    if resolved is None:
        return list(command)

    if sys.platform == "win32":
        lowered = resolved.lower()
        # Prefer a PowerShell shim (.ps1) in the same directory if present.
        # shutil.which honors PATHEXT which typically finds .bat/.cmd first,
        # but those shims re-interpret quoting and can break on long prompts.
        if lowered.endswith((".bat", ".cmd")):
            candidate = Path(resolved).with_suffix(".ps1")
            if candidate.exists():
                resolved = str(candidate)
                lowered = resolved.lower()

        if lowered.endswith(".ps1"):
            return ["pwsh", "-NoProfile", "-File", resolved, *tail]
        # For .bat / .cmd shims, invoke them directly. Python's subprocess on
        # Windows will spawn cmd.exe internally via CreateProcess, avoiding
        # the quoting pitfalls of an explicit "cmd /c" wrapper.

    return [resolved, *tail]


class CopilotCliRunner:
    def __init__(
        self,
        command: Sequence[str] | None = None,
        config_path: Path | None = None,
        extra_args: Sequence[str] | None = None,
    ):
        base = list(command) if command is not None else resolve_copilot_command(config_path)
        # Append default non-interactive flags only when using the vanilla
        # `copilot` executable and the caller did not already supply them.
        if command is None and extra_args is None and base and Path(base[0]).name.lower().startswith("copilot"):
            base = [*base, *DEFAULT_COPILOT_ARGS]
        elif extra_args:
            base = [*base, *extra_args]
        self.command = base

    def run(self, prompt: str) -> str:
        argv = _resolve_executable([*self.command, "-p", prompt])
        try:
            completed = subprocess.run(
                argv,
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
            )
        except FileNotFoundError as exc:
            raise RunnerInvocationError(
                f"Runner executable not found: {argv[0]!r}. "
                "Install GitHub Copilot CLI (https://github.com/github/copilot-cli) "
                "or set PAC_COPILOT_BIN to a different command."
            ) from exc

        if completed.returncode != 0:
            message = completed.stderr.strip() or completed.stdout.strip() or "Copilot runner failed."
            raise RunnerInvocationError(message)

        return completed.stdout.strip()
