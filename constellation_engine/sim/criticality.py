from __future__ import annotations

import networkx as nx

from constellation_engine.core.types import ServiceId
from constellation_engine.sim.models import FailureType
from constellation_engine.sim.propagate import propagate_failure


def compute_criticality(
    graph: nx.DiGraph,
    *,
    failure: FailureType = FailureType.DOWN,
) -> dict[ServiceId, int]:
    """
    Compute criticality for each service as the size of its blast radius.

    Criticality score = number of impacted services (including itself).
    """
    scores: dict[ServiceId, int] = {}

    for node in graph.nodes:
        impacted = propagate_failure(
            graph,
            start=node,
            failure=failure,
        )
        scores[node] = len(impacted)

    return scores