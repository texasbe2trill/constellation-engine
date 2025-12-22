from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore

from constellation_engine.core.types import (
    Service,
    Dependency,
    ServiceId,
    DependencyType,
    CallType,
)
from .schema import Manifest, ServiceSpec, DependencySpec


class ManifestError(ValueError):
    """Raised when a manifest is missing fields or has invalid values."""


def load_manifest(path: str | Path) -> Manifest:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))

    data = _read_yaml_or_json(p)

    if not isinstance(data, dict):
        raise ManifestError("Manifest root must be an object/dict.")

    services_raw = data.get("services")
    deps_raw = data.get("dependencies")

    if not isinstance(services_raw, list):
        raise ManifestError("'services' must be a list.")
    if not isinstance(deps_raw, list):
        raise ManifestError("'dependencies' must be a list.")

    services: list[ServiceSpec] = []
    for i, item in enumerate(services_raw):
        if not isinstance(item, dict):
            raise ManifestError(f"services[{i}] must be an object/dict.")
        sid = item.get("id")
        if not isinstance(sid, str) or not sid.strip():
            raise ManifestError(f"services[{i}].id must be a non-empty string.")
        services.append(
            ServiceSpec(
                id=sid,
                name=item.get("name") if isinstance(item.get("name"), str) else None,
                metadata=item.get("metadata") if isinstance(item.get("metadata"), dict) else None,
            )
        )

    deps: list[DependencySpec] = []
    for i, item in enumerate(deps_raw):
        if not isinstance(item, dict):
            raise ManifestError(f"dependencies[{i}] must be an object/dict.")
        src = item.get("src")
        dst = item.get("dst")
        if not isinstance(src, str) or not src.strip():
            raise ManifestError(f"dependencies[{i}].src must be a non-empty string.")
        if not isinstance(dst, str) or not dst.strip():
            raise ManifestError(f"dependencies[{i}].dst must be a non-empty string.")

        dep_type = item.get("dep_type", "hard")
        call_type = item.get("call_type", "sync")

        if not isinstance(dep_type, str):
            raise ManifestError(f"dependencies[{i}].dep_type must be a string.")
        if not isinstance(call_type, str):
            raise ManifestError(f"dependencies[{i}].call_type must be a string.")

        deps.append(
            DependencySpec(
                src=src,
                dst=dst,
                dep_type=dep_type,
                call_type=call_type,
                metadata=item.get("metadata") if isinstance(item.get("metadata"), dict) else None,
            )
        )

    return Manifest(services=services, dependencies=deps)


def manifest_to_domain(manifest: Manifest) -> tuple[list[Service], list[Dependency]]:
    services = [
        Service(id=ServiceId(s.id), name=s.name, metadata=s.metadata) for s in manifest.services
    ]

    dependencies: list[Dependency] = []
    for d in manifest.dependencies:
        dependencies.append(
            Dependency(
                src=ServiceId(d.src),
                dst=ServiceId(d.dst),
                dep_type=DependencyType(d.dep_type),
                call_type=CallType(d.call_type),
                metadata=d.metadata,
            )
        )

    return services, dependencies


def _read_yaml_or_json(path: Path) -> Any:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8")

    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    if suffix == ".json":
        return json.loads(text)

    raise ManifestError("Unsupported file extension. Use .yaml/.yml or .json.")