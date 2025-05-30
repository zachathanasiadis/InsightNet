from typing import Any, Protocol
from dataclasses import dataclass

class RoutingModel(Protocol):
    def get_out_edge(self, state):
        pass

    def get_direct_previous_states(self, state) -> list[Any]:
        raise NotImplementedError

@dataclass
class SkippingRoutingState:
    in_edge: int
    current_node: str

class SkippingRouting:
    def __init__(self) -> None:
    # dicitonary that maps skippingroutingstate to preference list of out_edges
        self.routing_table: dict[SkippingRoutingState,list[int]]
        self.failed_edges: list[int]

    # Note: this is where your implementation of the skipping routing should be
    def get_out_edge(self, state: SkippingRoutingState):
        # Hint: provide the chosen out-edge by selecting the first non failed edge in `state`
        pass
    def get_direct_previous_states(self, state) -> list[Any]:
        # DONE Note: why do you need `None`? Don't forget that an empty list is also a possible return value.
        raise NotImplementedError

    def add_routing_table(self):
        return

class CombinatorialRoutingState:
    pass

class CombinatorialRouting:
    def get_out_edge(self, state):
        pass
    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass

class Graph:
    # Note: This is technicly (almost) correct, but very impractical.
    # - One must build a complete graph with a forced structure before
    #   creating a Graph object. Consider adding methods to extend an empty graph.
    #   E.g., add_edge, add_node, ...
    # - There is no way of ensuring consistency. E.g., what happens if someone
    #   use edge endpoints that are not present in `nodes`?
    # - Consider adding other helper functions you can rely on later.
    #   E.g., get_edges_form(v), get_endpoins_of(e), ... be creative :)
    def __init__(self, nodes: list[str] = [], edges: list[int] = [], mapping: dict[int, tuple[str, str]] = {}) -> None:
        self.nodes = nodes
        self.edges = edges
        self.edge_to_node_mapping = mapping
        # Note: The whoule project aims to list possible failure
        # scenarios, so it shouldn't be required as input.
        # Hint: consider adding a `failed_links` parameter to
        # RoutingModel.get_out_edge

    def get_nodes(self) -> list[str]:
        return self.nodes

    def get_edges(self) -> list[int]:
        return self.edges

    def get_edege_to_node_mapping(self) -> dict[int, tuple[str, str]]:
        return self.edge_to_node_mapping

    def get_edges_from(self, node):
        edges_from_given_node = []
        for edge, node_tuple in self.edge_to_node_mapping.items():
            if node in node_tuple:
                edges_from_given_node.append(edge)
        return edges_from_given_node

    def get_nodes_from(self, edge):
        return self.edge_to_node_mapping[edge]

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def add_edge_to_node_mapping(self, edge_name, first_node, second_node):
        self.edge_to_node_mapping[edge_name] = (first_node, second_node)

class Network:
    def __init__(self, graph: Graph, routing_model: RoutingModel) -> None:
        self.graph: Graph = graph
        self.routing_model: RoutingModel = routing_model

    def get_all_paths_to(self, state) -> list[list[Any]]:
        raise NotImplementedError

def main() -> None:
    nodes = ["s", "v1", "v2", "v3", "v4", "d"]
    edges= [0,1,2,3,4,5,6]
    edge_to_node_mapping = {
        0 : ("s", "v1"),
        1 : ("s", "v3"),
        2 : ("v1", "v2"),
        3 : ("v3", "v4"),
        4 : ("v2", "v4"),
        5 : ("v2", "d"),
        6 : ("v4", "d")
    }

    graph = Graph()
    for node in nodes:
        graph.add_node(node)
    for edge in edges:
        graph.add_edge(edge)
    for edge, node_tuple in edge_to_node_mapping.items():
        graph.add_edge_to_node_mapping(edge, node_tuple[0], node_tuple[1])

if __name__ == "__main__":
    main()
