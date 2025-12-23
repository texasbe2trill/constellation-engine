from __future__ import annotations

import networkx as nx

from constellation_engine.core.types import CallType, DependencyType, ServiceId
from constellation_engine.sim.models import FailureType


def propagate_failure(
    graph: nx.DiGraph,
    *,
    start: ServiceId,
    failure: FailureType,
) -> dict[ServiceId, FailureType]:
    """
    Deterministically propagate a failure through the dependency graph.

    Rules (v0):
    - DOWN propagates through all outgoing edges
    - DEGRADED propagates only through HARD dependencies
    - LATENCY_UP propagates only through SYNC calls
    """
    impacted: dict[ServiceId, FailureType] = {start: failure}
    queue: list[ServiceId] = [start]

    while queue:
        current = queue.pop(0)

        for depender, _, attrs in graph.in_edges(current, data=True):
            dep_type: DependencyType = attrs["dep_type"]
            call_type: CallType = attrs["call_type"]

            if not _should_propagate(
                failure=failure,
                dep_type=dep_type,
                call_type=call_type,
            ):
                continue

            if depender not in impacted:
                impacted[depender] = impacted[current]
                queue.append(depender)

    return impacted


def _should_propagate(
    failure: FailureType,
    dep_type: DependencyType,
    call_type: CallType,
) -> bool:
    if failure == FailureType.DOWN:
        return True
    if failure == FailureType.DEGRADED:
        return dep_type == DependencyType.HARD
    if failure == FailureType.LATENCY_UP:
        return call_type == CallType.SYNC
    return False