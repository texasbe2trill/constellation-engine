from __future__ import annotations  # For future compatibility with type hinting

from dataclasses import dataclass  # For defining data classes
from typing import Any, Mapping  # For type hinting


@dataclass(frozen=True, slots=True)
class ServiceSpec:
    """Data class representing the schema of a service."""
    id: str  # Unique identifier for the service
    name: str | None = None  # Name of the service
    metadata: Mapping[str, Any] | None = None  # Additional metadata for the service

@dataclass(frozen=True, slots=True)
class DependencySpec:
    """Data class representing the schema of a dependency."""
    src: str  # Identifier of the dependent service
    dst: str  # Identifier of the service being depended on
    dep_type: str  # Type of the dependency
    call_type: str  # Type of call for the dependency
    metadata: Mapping[str, Any] | None = None  # Additional metadata for the dependency

@dataclass(frozen=True, slots=True)
class Manifest:
    """Data class representing the overall schema manifest."""
    services: list[ServiceSpec]  # List of service specifications
    dependencies: list[DependencySpec]  # List of dependency specifications