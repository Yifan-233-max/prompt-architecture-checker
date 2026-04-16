import os
import shlex
import tomllib
from pathlib import Path


def resolve_copilot_command(config_path: Path | None = None) -> list[str]:
    env_command = os.environ.get("PAC_COPILOT_BIN")
    if env_command:
        return shlex.split(env_command)

    config_path = config_path or Path("prompt-architecture-checker.toml")
    if config_path.exists():
        payload = tomllib.loads(config_path.read_text(encoding="utf-8"))
        configured = payload.get("runner", {}).get("command")
        if configured:
            return shlex.split(configured)

    return ["copilot"]
