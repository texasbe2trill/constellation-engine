from __future__ import annotations

from pathlib import Path

from constellation_engine.core.validate import validate_model
from constellation_engine.io.loaders import load_manifest, manifest_to_domain


def test_load_manifest_yaml_and_convert_to_domain(tmp_path: Path) -> None:
    p = tmp_path / "simple.yaml"
    p.write_text(
        """
services:
  - id: api
  - id: auth
  - id: db
dependencies:
  - src: api
    dst: auth
    dep_type: hard
    call_type: sync
  - src: auth
    dst: db
    dep_type: soft
    call_type: async
""".strip(),
        encoding="utf-8",
    )

    manifest = load_manifest(p)
    services, deps = manifest_to_domain(manifest)

    assert len(services) == 3
    assert len(deps) == 2

    result = validate_model(services, deps)
    assert result.ok