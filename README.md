# Constellation Engine

> A deterministic dependency reasoning engine for analyzing failure propagation in distributed systems

Constellation Engine is an open-source tool designed to model complex system architectures as explicit dependency graphs and compute failure blast radius before incidents occur. By focusing on system structure rather than runtime metrics, it provides deterministic answers to critical architectural questions: *What breaks when this service fails?*

## Core Capabilities

**Graph-Based System Modeling**
- Represents services and their dependencies as a directed graph
- Validates architectural definitions against invariants
- Supports complex topologies including microservices, workers, and infrastructure

**Failure Impact Analysis**
- Computes blast radius for different failure scenarios
- Ranks service criticality by downstream impact
- Provides deterministic, reproducible results

**Architectural Visibility**
- Makes hidden coupling and cascading failures explicit
- Identifies single points of failure
- Quantifies architectural risk before deployment

## What This Is Not

Constellation Engine is intentionally **not**:
- A monitoring or observability platform
- An alerting or incident response tool
- A probabilistic or ML-based system

It focuses purely on structural dependency analysis using deterministic rules.

## Quick Start

### Install

```bash
# From the repo root (editable for local development)
pip install -e .
# or install directly from a published wheel/sdist
pip install constellation-engine
```

This installs the `constellation-engine` console script defined in `pyproject.toml`.

### Basic Commands

```bash
# Validate system definition
constellation-engine validate docs/examples/simple.yaml

# View system statistics
constellation-engine stats docs/examples/simple.yaml

# Analyze blast radius for a service failure (flags are required)
constellation-engine blast-radius --service db --failure down docs/examples/simple.yaml
```

### Run Tests

```bash
python -m pytest -q
```
```text
.....                                                    [100%]
5 passed in 0.08s
```

## Enterprise Example

Constellation Engine includes a comprehensive enterprise architecture example at `docs/examples/enterprise.yaml` modeling a distributed e-commerce platform with 20+ services.

### Criticality Analysis

Identify which services have the highest downstream impact:

```bash
constellation-engine criticality docs/examples/enterprise.yaml
```
```text
criticality ranking (failure=down):
- postgres: impacts 18 services
- telemetry: impacts 16 services
- kafka: impacts 13 services
- audit-log: impacts 9 services
- redis: impacts 8 services
- elastic: impacts 8 services
- catalog: impacts 7 services
- orders: impacts 6 services
- payments: impacts 5 services
- inventory: impacts 5 services
```

### Blast Radius Analysis

Analyze the cascading impact of critical infrastructure failures:

**Scenario: PostgreSQL Database Failure**
```bash
constellation-engine blast-radius --service postgres --failure down docs/examples/enterprise.yaml
```
Both `--service` and `--failure` are required flags; omitting either will return a usage error.
```text
blast radius from postgres (down) [impacts dependers]:
- postgres: down
- user: down
- auth: down
- catalog: down
- payments: down
- orders: down
- inventory: down
- shipping: down
- orders-worker-1: down
- orders-worker-2: down
- orders-worker-3: down
- api-gateway: down
- catalog-read-us: down
- catalog-read-eu: down
- catalog-read-apac: down
- checkout: down
- web-frontend: down
- mobile-api: down
```

*Result: 17 of 20 services impacted by a single database failure — a critical architectural dependency.*

## Architecture

### Dependency Semantics
Edges in the dependency graph are defined as:
```
src → dst  means  "src depends on dst"
```

When `dst` fails, `src` becomes impacted. This simple semantic enables deterministic propagation analysis.

### Project Structure
```
constellation_engine/
├── cli/          # Command-line interface
├── core/         # Graph modeling and validation
├── io/           # Manifest loading and schema validation
└── sim/          # Failure propagation and criticality analysis
```

## Use Cases

- **Pre-Production Architecture Review**: Identify critical dependencies before deployment
- **Incident Response Planning**: Understand blast radius for incident scenarios
- **System Design Validation**: Quantify the impact of architectural decisions
- **Risk Assessment**: Identify single points of failure in distributed systems

## Development Status

Constellation Engine is under active development. The current version provides deterministic dependency modeling and failure propagation analysis. Future enhancements may include advanced graph algorithms and integration capabilities.

## License

This project is open source. See [LICENSE](LICENSE) for details.
