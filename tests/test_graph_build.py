import networkx as nx

from constellation_engine.core.types import Service, Dependency, ServiceId, DependencyType, CallType
from constellation_engine.core.validate import validate_or_raise
from constellation_engine.core.graph import build_graph

def test_build_graph_has_expected_nodes_edges_and_attributes():
    services = [
        Service(ServiceId("api")),
        Service(ServiceId("auth")),
        Service(ServiceId("db")),
    ]

    dependencies = [
        Dependency(
            src=ServiceId("api"),
            dst=ServiceId("auth"),
            dep_type=DependencyType.HARD,
            call_type=CallType.SYNC,
        ),
        Dependency(
            src=ServiceId("auth"),
            dst=ServiceId("db"),
            dep_type=DependencyType.SOFT,
            call_type=CallType.ASYNC,
        ),
    ]
    # Validate the model before building the graph
    validate_or_raise(services, dependencies)

    g = build_graph(services, dependencies) # Build the dependency graph

    assert isinstance(g, nx.DiGraph) # Check if the graph is a directed graph
    assert g.number_of_nodes() == 3 # Check the number of nodes
    assert g.number_of_edges() == 2 # Check the number of edges
    
    assert g.has_edge(ServiceId("api"), ServiceId("auth")) # Check for specific edge
    assert g.has_edge(ServiceId("auth"), ServiceId("db")) # Check for specific edge

    # Edge attributes preserved
    api_auth = g.get_edge_data(ServiceId("api"), ServiceId("auth"))
    assert api_auth["dep_type"] == DependencyType.HARD
    assert api_auth["call_type"] == CallType.SYNC

    auth_db = g.edges[ServiceId("auth"), ServiceId("db")]
    assert auth_db["dep_type"] == DependencyType.SOFT
    assert auth_db["call_type"] == CallType.ASYNC