# Security Policy

We value the security of Constellation Engine users. Please follow the guidance below for reporting vulnerabilities and handling security issues.

## Reporting a vulnerability

- Contact: Chris Campbell (texasbe2trill) via BlueSky direct message
- If possible, also open a private GitHub security advisory for coordinated disclosure.
- Include:
  - A description of the issue and impact
  - Steps or a manifest/command to reproduce
  - Any suggested fixes or mitigations
  - Your environment details (OS, Python version, commit/branch)

## Expectations

- We will acknowledge receipt within 5 business days.
- We aim to provide an initial assessment and remediation plan within 10 business days where feasible.
- Please keep reports confidential until a fix is released and coordinated disclosure is agreed.

## Scope

- Vulnerabilities in the CLI, core library, loaders, and simulation logic.
- Supply chain concerns in packaging (PyPI artifacts, `pyproject.toml`).

## Out of scope

- Issues in third-party dependencies (report upstream where appropriate).
- Operational topics for self-hosted environments (infrastructure hardening, host security, etc.).
