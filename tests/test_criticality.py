from constellation_engine.core.types import Service, Dependency, ServiceId
from constellation_engine.core.graph import build_graph
from constellation_engine.sim.criticality import compute_criticality
from constellation_engine.sim.models import FailureType


def test_criticality_ranks_shared_dependency_highest() -> None:
    services = [
        Service(ServiceId("a")),
        Service(ServiceId("b")),
        Service(ServiceId("c")),
    ]
    dependencies = [
        Dependency(ServiceId("a"), ServiceId("c")),
        Dependency(ServiceId("b"), ServiceId("c")),
    ]

    g = build_graph(services, dependencies)

    scores = compute_criticality(g, failure=FailureType.DOWN)

    assert scores[ServiceId("c")] == 3
    assert scores[ServiceId("a")] == 1
    assert scores[ServiceId("b")] == 1