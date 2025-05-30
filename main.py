from typing import Any, Protocol
from dataclasses import dataclass

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

class RoutingModel(Protocol):
    def get_out_edge(self, state) -> int | None:
        raise NotImplementedError

    def get_direct_previous_states(self, graph, state) -> list[Any]:
        raise NotImplementedError

# dataclasses are not hashable by design, unsafe_hash is a workaround. Otherwise dataclass should become frozen (immutable)
# which doesn't fit our use case
@dataclass(unsafe_hash=True)
class SkippingRoutingState:
    in_edge: int | None
    current_node: str

class SkippingRouting:
    def __init__(self, routing_table: dict[SkippingRoutingState,list[int]] = {}, failed_edges: list[int] =[]) -> None:
    # dicitonary that maps skippingroutingstate to preference list of out_edges
        self.routing_table: dict[SkippingRoutingState,list[int]] = routing_table
        self.failed_edges: list[int] = failed_edges

    # Note: this is where your implementation of the skipping routing should be
    def get_out_edge(self, state: SkippingRoutingState) -> int | None:
        # Hint: provide the chosen out-edge by selecting the first non failed edge in `state`
        for node in self.routing_table[state]:
            if node not in self.failed_edges:
                return node
        return None
    def get_direct_previous_states(self, graph: Graph, state: SkippingRoutingState) -> list[Any]:
        # DONE Note: why do you need `None`? Don't forget that an empty list is also a possible return value.
        previous_states= []
        nodes_connected_to_edge= graph.get_nodes_from(state.in_edge)
        previous_node = None
        for node in nodes_connected_to_edge:
            if node != state.current_node:
                previous_node = node
        edges_connected_to_previous_node = graph.get_edges_from(previous_node)
        for edges in edges_connected_to_previous_node:
            previous_states.append((edges,previous_node))
        return previous_states

    def add_routing_table(self, state: SkippingRoutingState, routing_table_of_node: list[int]):
        self.routing_table[state] = routing_table_of_node

class CombinatorialRoutingState:
    pass

class CombinatorialRouting:
    def get_out_edge(self, state) -> int | None:
        pass
    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass

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

    routing_table = {
        (None, "s") : [1, 0],
        (0, "s") : [1, 0],
        (None, "v1") : [2, 0],
        (0, "v1") : [2, 0],
        (2, "v1") : [0, 2],
        (None, "v2") : [5, 4, 2],
        (4, "v2") : [5, 2, 4],
        (2, "v2") : [5, 4, 2],
        (None, "v3") : [3, 1],
        (3, "v3") : [1, 3],
        (None, "v4") : [6, 3, 4],
        (4, "v4") : [6, 3, 4],
        (3, "v4") : [6, 4, 3],
        (6, "v4") : [3, 4, 6],
        (None, "d") : [5, 6],
        (6, "d") : [5, 6]
    }

    state = SkippingRoutingState(0, "s")
    skipping_routing = SkippingRouting()
    skipping_routing.add_routing_table(state, routing_table[(state.in_edge,state.current_node)])
    print(skipping_routing.routing_table)
    print(skipping_routing.get_out_edge(state))
    print(skipping_routing.get_direct_previous_states(graph, state))

    network = Network(graph, skipping_routing)

if __name__ == "__main__":
    main()
