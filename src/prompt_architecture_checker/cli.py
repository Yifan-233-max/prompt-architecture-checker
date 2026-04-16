import argparse
import sys
from pathlib import Path
from typing import Sequence

from .orchestrator import run_parse, run_report, run_review
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


def main(
    argv: Sequence[str] | None = None,
    runner: SkillRunner | None = None,
    stdout=None,
) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    runner = runner or CopilotCliRunner()
    stdout = stdout or sys.stdout
    repo_path = Path(args.repo)

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
        parse_artifact, review_artifact = run_review(repo_path, runner)
        print(
            f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
            file=stdout,
        )
        print("Reviewing...", file=stdout)
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
    parse_artifact, review_artifact, report_artifact = run_report(repo_path, runner)
    print(
        f"Parse complete: {len(parse_artifact.summary)} summary items, {len(parse_artifact.graph)} graph edges",
        file=stdout,
    )
    print("Reviewing...", file=stdout)
    print(
        f"Review complete: {len(review_artifact.findings)} findings",
        file=stdout,
    )
    print("Reporting...", file=stdout)
    body = render_report(report_artifact)
    print("Report complete: markdown ready", file=stdout)
    print(body, file=stdout)
    if args.out_path:
        write_output(Path(args.out_path), body)
    return 0
