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

    return 1


if __name__ == "__main__":
    raise SystemExit(main())