# Import Statements
from __future__ import annotations  # For future compatibility with type hinting

from dataclasses import dataclass  # For defining data classes
from typing import Iterable  # For type hinting

from .types import Dependency, Service, ServiceId  # Importing types from the same package


class ValidationError(Exception):
    """Raised when the dependency model violates Constellation"""

@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Data class representing the result of a validation process."""
    ok: bool # Indicates if the model is valid
    errors: tuple[str, ...] # List of error messages if any

def validate_model(
    services: Iterable[Service],
    dependencies: Iterable[Dependency],
    *,
    allow_self_dependencies: bool = False,
) -> ValidationResult:
    """Validates the given services and dependencies against Constellation rules.

    Args:
        services: An iterable of Service objects to validate.
        dependencies: An iterable of Dependency objects to validate.
        allow_self_dependencies: If True, allows services to depend on themselves. """
    errors: list[str] = []

    services_list = list(services)
    deps_list = list(dependencies)

    # 1) Check for unique service IDs
    ids = [svc.id for svc in services_list] # Extract service IDs
    seen: set[ServiceId] = set() # Set to track seen IDs
    dupes: set[ServiceId] = set() # Set to track duplicate IDs
    for sid in ids:
        if sid in seen:
            dupes.add(sid)
        else:
            seen.add(sid)
    if dupes:
        errors.append(f"Duplicate service IDs found: {sorted(str(x) for x in dupes)}")
    
    service_ids = set(ids) # Set of valid service IDs

    # 2) Validate dependencies endpoints exist
    for d in deps_list:
        if d.src not in service_ids:
            errors.append(f"Dependency source {d.src} does not exist among services.")
        if d.dst not in service_ids:
            errors.append(f"Dependency destination {d.dst} does not exist among services.")
    # 3) Check for self-dependencies if not allowed
    if not allow_self_dependencies:
        for d in deps_list:
            if d.src == d.dst:
                errors.append(f"Service {d.src} has a self-dependency, which is not allowed.")

    return ValidationResult(ok=(len(errors) == 0), errors=tuple(errors)) # Return validation result

def validate_or_raise(
    services: Iterable[Service],
    dependencies: Iterable[Dependency],
    *,
    allow_self_dependencies: bool = False,
) -> None:
    """Validates the given services and dependencies, raising ValidationError on failure.

    Args:
        services: An iterable of Service objects to validate.
        dependencies: An iterable of Dependency objects to validate.
        allow_self_dependencies: If True, allows services to depend on themselves.
    Raises:
        ValidationError: If the validation fails.
    """
    result = validate_model(
        services,
        dependencies,
        allow_self_dependencies=allow_self_dependencies,
    )
    if not result.ok:
        msg = "Validation failed with the following errors:\n" + "\n".join(result.errors)
        raise ValidationError(msg)