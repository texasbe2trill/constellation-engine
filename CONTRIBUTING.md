# Contributing to Constellation Engine

Thanks for helping improve Constellation Engine! This project is focused on deterministic dependency modeling, blast-radius analysis, and criticality scoring. Contributions that improve correctness, clarity, and usability are welcome.

## Development setup

1) Clone and install in editable mode with dev extras:
```
pip install -e ".[dev]"
```
2) Use Python 3.11+ (matches CI matrix 3.11/3.12).

## Tests, lint, type-check

- Run tests: `pytest -q`
- Lint: `ruff check .`
- Type-check: `mypy constellation_engine`

CI runs the same steps in `.github/workflows/ci.yml`.

## Adding or updating examples

- Examples live in `docs/examples/` (e.g., `simple.yaml`, `enterprise.yaml`).
- Keep manifests small and readable; prefer meaningful service names and minimal metadata.
- Ensure new examples validate: `constellation-engine validate docs/examples/<file>.yaml`.
- If you change examples, update any referenced docs or snippets that show expected CLI output.

## Pull request guidelines

- Keep changes focused; small, reviewable PRs are easiest to merge.
- Include tests for new behavior or bug fixes (validation, propagation, criticality, CLI parsing, loaders, etc.).
- Run lint + type + tests locally before opening the PR.
- Update docs/README/release notes when user-facing behavior changes (CLI flags, outputs, failure rules).

## Reporting bugs

- Provide a minimal manifest and the exact CLI command that reproduces the issue.
- Include expected vs. actual output.
- Note your OS, Python version, and commit/branch if relevant.
