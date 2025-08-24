from typing import Any
from .graph import Graph


def parse_graph(data: dict[str, Any]) -> Graph:
    graph = Graph()
    for node in data["nodes"]:
        graph.add_node(node)
    for entry in data["edge_to_node_mapping"]:
        graph.add_edge(entry["edge"], entry["nodes"][0], entry["nodes"][1])
    return graph
