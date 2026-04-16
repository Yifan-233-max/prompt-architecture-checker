import argparse
import sys
from pathlib import Path
from typing import Sequence

from .orchestrator import (
    StageExecutionError,
    run_parse,
    run_report,
    run_report_stage,
    run_review,
    run_review_stage,
)
from .output import render_parse, render_report, render_review, write_output
from .runner import CopilotCliRunner, SkillRunner


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-architecture-checker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("parse", "review", "report"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("repo")
        subparser.add_argument("--out", dest="out_path")

    return parser


def _validate_repo_path(repo_path: Path) -> str | None:
    if not repo_path.exists():
        return f"Repository path does not exist: {repo_path}"
    if not repo_path.is_dir():
        return f"Repository path is not a directory: {repo_path}"
    return None


def main(
    argv: Sequence[str] | None = None,
    runner: SkillRunner | None = None,
    stdout=None,
    stderr=None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    runner = runner or CopilotCliRunner()
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    repo_path = Path(args.repo)

    validation_error = _validate_repo_path(repo_path)
    if validation_error is not None:
        print(validation_error, file=stderr)
        return 2

    try:
        if args.command == "parse":
            print("Parsing...", file=stdout)
            artifact = run_parse(repo_path, runner)
            body = render_parse(artifact)
            print(
                f"Parse complete: {len(artifact.summary)} summary items, {len(artifact.graph)} graph edges",
                file=stdout,
            )
            print(body, file=stdout)
            if args.out_path:
                write_output(Path(args.out_path), body)
            return 0

        if args.command == "review":
            print("Parsing...", file=stdout)
            parse_artifact = run_parse(repo_path, runner)
            print(
                f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
                file=stdout,
            )
            print("Reviewing...", file=stdout)
            review_artifact = run_review_stage(repo_path, runner, parse_artifact)
            body = render_review(review_artifact)
            print(
                f"Review complete: {len(review_artifact.findings)} findings",
                file=stdout,
            )
            print(body, file=stdout)
            if args.out_path:
                write_output(Path(args.out_path), body)
            return 0

        print("Parsing...", file=stdout)
        parse_artifact = run_parse(repo_path, runner)
        print(
            f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
            file=stdout,
        )
        print("Reviewing...", file=stdout)
        review_artifact = run_review_stage(repo_path, runner, parse_artifact)
        print(
            f"Review complete: {len(review_artifact.findings)} findings",
            file=stdout,
        )
        print("Reporting...", file=stdout)
        report_artifact = run_report_stage(repo_path, runner, parse_artifact, review_artifact)
        body = render_report(report_artifact)
        print("Report complete: markdown ready", file=stdout)
        print(body, file=stdout)
        if args.out_path:
            write_output(Path(args.out_path), body)
        return 0
    except StageExecutionError as exc:
        print(f"{exc.stage} stage failed: {exc}", file=stderr)
        return 1
