# Import statements
from __future__ import annotations # For future compatibility with type hinting

from dataclasses import dataclass # For defining data classes
from enum import Enum # For creating enumerations
from typing import NewType, Mapping, Any # For type hinting

ServiceId = NewType("ServiceId", str) # New type for service identifiers

class DependencyType(str, Enum):
    """Enumeration of different types of dependencies."""
    HARD = "hard" # Hard dependency
    SOFT = "soft" # Soft dependency
    OPTIONAL = "optional" # Optional dependency

class CallType(str, Enum):
    """Enumeration of different types of call types."""
    SYNC = "sync" # Synchronous call
    ASYNC = "async" # Asynchronous call

@dataclass(frozen=True, slots=True)
class Service:
    """Data class representing a service with its attributes."""
    id: ServiceId # Unique identifier for the service
    name: str | None = None # Name of the service
    metadata: Mapping[str, Any] | None = None # Additional metadata for the service

@dataclass(frozen=True, slots=True)
class Dependency:
    """Data class representing a dependency with its attributes."""
    src: ServiceId # Identifier of the dependent service
    dst: ServiceId # Identifier of the service being depended on
    dep_type: DependencyType = DependencyType.HARD # Type of the dependency
    call_type: CallType = CallType.SYNC # Type of call for the dependency
    metadata: Mapping[str, Any] | None = None # Additional metadata for the dependency