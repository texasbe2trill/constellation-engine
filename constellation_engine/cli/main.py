from __future__ import annotations

import argparse

from constellation_engine.core.graph import build_graph
from constellation_engine.core.validate import validate_model
from constellation_engine.io.loaders import load_manifest, manifest_to_domain


def main() -> int:
    parser = argparse.ArgumentParser(prog="constellation-engine")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_validate = sub.add_parser("validate", help="Validate a manifest.")
    p_validate.add_argument("path", help="Path to .yaml/.yml/.json manifest")

    p_stats = sub.add_parser("stats", help="Show basic graph stats from a manifest.")
    p_stats.add_argument("path", help="Path to .yaml/.yml/.json manifest")

    p_blast = sub.add_parser("blast-radius", help="Compute blast radius from a failure.")
    p_blast.add_argument("path", help="Path to manifest file")
    p_blast.add_argument("--service", required=True, help="Service ID to fail")
    p_blast.add_argument(
        "--failure",
        required=True,
        choices=["down", "degraded", "latency_up"],
        help="Failure type",
    )

    p_crit = sub.add_parser(
    "criticality",
    help="Rank services by blast radius size (most critical first).",
    )
    p_crit.add_argument("path", help="Path to manifest file")
    p_crit.add_argument(
        "--failure",
        choices=["down", "degraded", "latency_up"],
        default="down",
        help="Failure type to evaluate (default: down)",
    )
    p_crit.add_argument(
        "--top",
        type=int,
        default=10,
        help="Show top N most critical services",
    )

    args = parser.parse_args()

    manifest = load_manifest(args.path)
    services, deps = manifest_to_domain(manifest)

    if args.cmd == "validate":
        result = validate_model(services, deps)
        if result.ok:
            print("OK: manifest is valid")
            return 0
        print("INVALID:")
        for e in result.errors:
            print(f"- {e}")
        return 2

    if args.cmd == "stats":
        g = build_graph(services, deps)
        print(f"nodes: {g.number_of_nodes()}")
        print(f"edges: {g.number_of_edges()}")
        # simple, deterministic summary
        top = sorted(g.out_degree(), key=lambda x: x[1], reverse=True)[:5]
        print("top dependers (out-degree):")
        for node, deg in top:
            print(f"- {node}: {deg}")
        return 0
    
    if args.cmd == "blast-radius":
        from constellation_engine.core.types import ServiceId
        from constellation_engine.sim.models import FailureType
        from constellation_engine.sim.propagate import propagate_failure

        g = build_graph(services, deps)

        impacted = propagate_failure(
            g,
            start=ServiceId(args.service),
            failure=FailureType(args.failure),
        )

        print(f"blast radius from {args.service} ({args.failure}) [impacts dependers]:")
        for svc, f in impacted.items():
            print(f"- {svc}: {f.value}")
        return 0
    
    if args.cmd == "criticality":
        from constellation_engine.sim.criticality import compute_criticality
        from constellation_engine.sim.models import FailureType

        g = build_graph(services, deps)

        scores = compute_criticality(
            g,
            failure=FailureType(args.failure),
        )

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        print(f"criticality ranking (failure={args.failure}):")
        for svc, score in ranked[: args.top]:
            print(f"- {svc}: impacts {score} services")

        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())