from prompt_architecture_checker.cli import build_parser


def test_build_parser_exposes_parse_review_report_subcommands():
    parser = build_parser()
    subparsers_action = next(
        action for action in parser._actions if getattr(action, "choices", None)
    )

    assert set(subparsers_action.choices) == {"parse", "review", "report"}
