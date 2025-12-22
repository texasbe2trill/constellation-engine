from __future__ import annotations

from constellation_engine.core.types import (
    Service,
    Dependency,
    ServiceId,
    DependencyType,
    CallType,
)
from constellation_engine.core.graph import build_graph
from constellation_engine.sim.models import FailureType
from constellation_engine.sim.propagate import propagate_failure


def test_down_failure_propagates_to_all_downstream_services() -> None:
    services = [
        Service(ServiceId("api")),
        Service(ServiceId("auth")),
        Service(ServiceId("db")),
    ]

    dependencies = [
        Dependency(ServiceId("api"), ServiceId("auth")),
        Dependency(ServiceId("auth"), ServiceId("db")),
    ]

    g = build_graph(services, dependencies)

    impacted = propagate_failure(
        g,
        start=ServiceId("db"),
        failure=FailureType.DOWN,
    )

    assert set(impacted.keys()) == {
        ServiceId("db"),
        ServiceId("auth"),
        ServiceId("api"),
    }

def test_auth_down_impacts_api_not_db() -> None:
    services = [
        Service(ServiceId("api")),
        Service(ServiceId("auth")),
        Service(ServiceId("db")),
    ]
    dependencies = [
        Dependency(ServiceId("api"), ServiceId("auth")),
        Dependency(ServiceId("auth"), ServiceId("db")),
    ]
    g = build_graph(services, dependencies)

    impacted = propagate_failure(g, start=ServiceId("auth"), failure=FailureType.DOWN)

    assert set(impacted.keys()) == {ServiceId("auth"), ServiceId("api")}