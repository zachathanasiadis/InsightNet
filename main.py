from typing import Any, Protocol
from dataclasses import dataclass

class RoutingModel(Protocol):
    # DONE Note: avoid spaces/tabs at the end of lines, your IDE probably has an autoformat feature to take care of the problem
    def get_out_edge(self, state):
        pass

    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass

@dataclass
class SkippingRoutingState:
    # DONE Note: consider using a dataclass: https://docs.python.org/3/library/dataclasses.html
    in_edge: int
    current_node: str
    out_edges: list[int]

class SkippingRouting:
    # Note: this is where your implementation of the skipping routing should be
    def get_out_edge(self, state: SkippingRoutingState):
        # Hint: provide the chosen out-edge by selecting the first non failed edge in `state`
        pass
    def get_direct_previous_states(self, state):
        # DONE Note: why do you need `None`? Don't forget that an empty list is also a possible return value.
        pass

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
    def __init__(self, nodes: list[str], edges: list[int], mapping: dict[int, tuple[str, str]]) -> None:
        self.nodes = nodes
        self.edges = edges
        self.mapping = mapping
        # Note: The whoule project aims to list possible failure
        # scenarios, so it shouldn't be required as input.
        # Hint: consider adding a `failed_links` parameter to
        # RoutingModel.get_out_edge

    def get_nodes(self) -> list[str]:
        return self.nodes

    def get_edges(self) -> list[int]:
        return self.edges

    def get_mapping(self) -> dict[int, tuple[str, str]]:
        return self.mapping

class Network:
    def __init__(self, graph: Graph, routing_model: RoutingModel) -> None:
        self.graph: Graph = graph
        self.routing_model: RoutingModel = routing_model

    def get_all_paths_to(self, state) -> list[list[Any]] | None:
        pass

    def get_path_to(self, source: SkippingRoutingState, destination: SkippingRoutingState):
        pass

def main() -> None:
    # DONE Note: in general, try to avoid function-in-function definitions
    # unless you have a very good reason to do so. It has a big cost
    # in terms of readibility and testability.
    # Note: Why are these functions here? Why not put them in the relevant classes?

    nodes = ["s", "v1", "v2", "v3", "v4", "d"]
    edges= [0,1,2,3,4,5,6]
    mapping = {
        0 : ("s", "v1"),
        1 : ("s", "v3"),
        2 : ("v1", "v2"),
        3 : ("v3", "v4"),
        4 : ("v2", "v4"),
        5 : ("v2", "d"),
        6 : ("v4", "d")
    }


    skipping_routing_path = get_path_to("s","d")


    routing_model: RoutingModel = SkippingRouting()
    graph = Graph(nodes, edges, mapping)
    network = Network(graph, routing_model)

if __name__ == "__main__":
    main()
