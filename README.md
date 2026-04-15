# Prompt Architecture Reviewer Skill

Review prompt-as-code repositories for contract, flow, and architecture-pattern weaknesses before runtime.

## What This Repository Ships

- `SKILL.md`: the public skill entrypoint
- `reviewer-prompt.md`: the detailed review procedure
- `output-format.md`: the canonical findings model and report shape
- `examples/`: positive, negative, and mixed review fixtures

## What The Skill Reviews

The skill is designed to review an entire prompt-as-code repository and surface:

- missing or weak contracts
- ambiguous or fragile handoffs
- hidden state dependencies
- architecture-pattern weaknesses
- reviewability gaps where the repository is too implicit to assess reliably

## What The Skill Does Not Try To Do

- run the target repository
- rewrite prompts automatically
- act like a broad security scanner
- prioritize tone or style over architecture correctness

## Example Invocation

```text
Review this prompt-as-code repository. Focus on contract, flow, and architecture-pattern issues. Give me a severity-ranked findings list with evidence and suggested fixes.
```

## Repository Layout

- `SKILL.md`
- `reviewer-prompt.md`
- `output-format.md`
- `examples/good-repo/`
- `examples/bad-repo/`
- `examples/mixed-repo/`

## Review Output Contract

Every finding should include:

- severity
- findingClass
- category
- artifactScope
- message
- evidence
- whyItMatters
- suggestedFix

## License

This repository is released under the MIT License.
