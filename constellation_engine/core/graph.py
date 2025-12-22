from __future__ import annotations  # For future compatibility with type hinting
import networkx as nx  # Importing NetworkX for graph operations

from .types import Service, Dependency, ServiceId # Importing types from the same package
from .validate import validate_or_raise # Importing validation function

def build_graph(services: list[Service], dependencies: list[Dependency]) -> nx.DiGraph:
    """Builds a directed graph from the given services and dependencies.

    Args:
        services: A list of Service objects representing the nodes.
        dependencies: A list of Dependency objects representing the edges."""
    validate_or_raise(services, dependencies)  # Validate the model before building the graph
    
    g: nx.DiGraph = nx.DiGraph()  # Initialize a directed graph

    # Add services as nodes
    for svc in services:
        g.add_node(svc.id, name=svc.name, metadata=svc.metadata)

    # Add dependencies as edges
    for dep in dependencies:
        g.add_edge(
            dep.src,
            dep.dst,
            dep_type=dep.dep_type,
            call_type=dep.call_type,
            metadata=dep.metadata,
        )

    return g  # Return the constructed graph