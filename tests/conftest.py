from pathlib import Path

import pytest


class StubRunner:
    def __init__(self, responses: list[str]):
        self.responses = list(responses)
        self.prompts: list[str] = []

    def run(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.responses.pop(0)


@pytest.fixture
def sample_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# sample repo\n", encoding="utf-8")
    return repo


@pytest.fixture
def stub_runner_factory():
    def factory(*responses: str) -> StubRunner:
        return StubRunner(list(responses))

    return factory
