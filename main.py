from typing import Any, Protocol
from dataclasses import dataclass


@dataclass(frozen=True)
class SkippingRoutingState:
    in_edge: int | None
    current_node: str


class CombinatorialRoutingState:
    pass


class Graph:
    def __init__(
        self,
        nodes: list[str] = [],
        edges: list[int] = [],
        edge_to_node_mapping: dict[int, tuple[str, str]] = {},
    ) -> None:
        self.nodes = nodes
        self.edges = edges
        self.edge_to_node_mapping = edge_to_node_mapping

    def get_nodes(self) -> list[str]:
        return self.nodes

    def get_edges(self) -> list[int]:
        return self.edges

    def get_edge_to_node_mapping(self) -> dict[int, tuple[str, str]]:
        return self.edge_to_node_mapping

    def get_edges_from_node(self, node: str) -> list[int]:
        return [
            edge
            for edge, node_tuple in self.edge_to_node_mapping.items()
            if node in node_tuple
        ]

    def get_endpoints_of_edge(self, edge: int) -> set[str]:
        return set(self.edge_to_node_mapping[edge])

    def add_node(self, node: str) -> None:
        self.nodes.append(node)

    def add_edge(self, edge_id: int, v1: str, v2: str) -> None:
        self.edge_to_node_mapping[edge_id] = (v1, v2)
        self.edges.append(edge_id)


class RoutingModel(Protocol):
    def get_out_edge(self, state, failed_edges) -> int | None:
        raise NotImplementedError

    def get_direct_previous_states(self, graph, state) -> list[Any]:
        raise NotImplementedError


class SkippingRouting:
    def __init__(
        self,
        routing_table: dict[SkippingRoutingState, list[int]] = {},
    ) -> None:
        self.routing_table: dict[SkippingRoutingState, list[int]] = routing_table

    def is_valid_state(self,state: SkippingRoutingState) -> None:
        if state not in self.routing_table:
            raise Exception("Invalid state")

    def get_out_edge(
        self, state: SkippingRoutingState, failed_edges: list[int]
    ) -> int | None:
        for node in self.routing_table[state]:
            if node not in failed_edges:
                return node
        return None

    def get_direct_previous_states(
        self, graph: Graph, state: SkippingRoutingState
    ) -> list[SkippingRoutingState]:
        previous_states = []
        nodes_connected_to_edge = []
        if state.in_edge is None:
            return []
        # Finding previous node
        nodes_connected_to_edge = graph.get_endpoints_of_edge(state.in_edge)
        previous_node = state.current_node
        for node in nodes_connected_to_edge:
            if node != state.current_node:
                previous_node = node
        # Finding possible previous edges
        if (
            state.in_edge
            in self.routing_table[SkippingRoutingState(None, previous_node)]
        ):
            previous_states.append(SkippingRoutingState(None, previous_node))
        for edge in graph.get_edges_from_node(previous_node):
            candidate = SkippingRoutingState(edge, previous_node)
            if self.routing_table.get(candidate):
                if state.in_edge in self.routing_table[candidate]:
                    previous_states.append(candidate)
        return previous_states

    def update_routing_table(
        self,
        state: SkippingRoutingState,
        graph: Graph,
        routing_table_of_node: list[int],
    ) -> None:
        if state not in self.routing_table:
            self.routing_table[state] = []
        for edge in routing_table_of_node:
            if edge not in graph.get_edges():
                raise Exception("Edge in not Graph")
            # TODO finish checks
            self.routing_table[state].append(edge)


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
    nodes = ["v0", "v1", "v2", "v3", "v4", "v5"]
    edge_to_node_mapping = {
        0: ("v1", "v1"),
        1: ("v0", "v3"),
        2: ("v1", "v2"),
        3: ("v3", "v4"),
        4: ("v2", "v4"),
        5: ("v2", "v5"),
        6: ("v4", "v5"),
    }

    graph = Graph()
    for node in nodes:
        graph.add_node(node)
    for edge, node_tuple in edge_to_node_mapping.items():
        graph.add_edge(edge, node_tuple[0], node_tuple[1])

    routing_table = {
        (None, "v0"): [1, 0],
        (0, "v0"): [1, 0],
        (None, "v1"): [2, 0],
        (0, "v1"): [2, 0],
        (2, "v1"): [0, 2],
        (None, "v2"): [5, 4, 2],
        (4, "v2"): [5, 2, 4],
        (2, "v2"): [5, 4, 2],
        (None, "v3"): [3, 1],
        (3, "v3"): [1, 3],
        (None, "v4"): [6, 3, 4],
        (4, "v4"): [6, 3, 4],
        (3, "v4"): [6, 4, 3],
        (6, "v4"): [3, 4, 6],
        (None, "v5"): [5, 6],
        (6, "v5"): [5, 6],
    }

    state = SkippingRoutingState(4, "v4")
    skipping_routing = SkippingRouting()
    for routing_table_state, routing_table__pref_list in routing_table.items():
        skipping_routing.update_routing_table(
            SkippingRoutingState(routing_table_state[0], routing_table_state[1]),
            graph,
            routing_table__pref_list,
        )
    skipping_routing.is_valid_state(state)
    print(skipping_routing.get_direct_previous_states(graph, state))
    # Zach: for state with in_edge= 4 and current_node= "v4" the direct previous states
    # are [(None, "v2"), (2, "v2"), (4, "v2")]
    #
    # Csaba: [(2, 'v2'), (None, 'v2')]
    network = Network(graph, skipping_routing)


if __name__ == "__main__":
    main()
