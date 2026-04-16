import argparse
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-architecture-checker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("parse", "review", "report"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("repo")
        subparser.add_argument("--out", dest="out_path")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    return 0
