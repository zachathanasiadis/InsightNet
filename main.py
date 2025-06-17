from typing import Any, Protocol
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class SkippingRoutingState:
    in_edge: int | None
    current_node: str


class CombinatorialRoutingState:
    pass


class Graph:
    def __init__(self, nodes: list[str] = [], edges: list[int] = [], edge_to_node_mapping: dict[int, tuple[str, str]] = {}) -> None:
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
        return [edge for edge, node_tuple in self.edge_to_node_mapping.items() if node in node_tuple]

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

    def get_direct_previous_states(self, state) -> list[Any]:
        raise NotImplementedError


class SkippingRouting:
    def __init__(self, graph: Graph, routing_table: dict[SkippingRoutingState, list[int]] = {}) -> None:
        self.graph = graph
        self.routing_table: dict[SkippingRoutingState,
                                 list[int]] = routing_table

    def get_out_edge(self, state: SkippingRoutingState, failed_edges: list[int] = []) -> int | None:
        for node in self.routing_table[state]:
            if node not in failed_edges:
                return node
        return None

    def get_direct_previous_states(self, state: SkippingRoutingState) -> list[SkippingRoutingState]:
        previous_states = []
        nodes_connected_to_edge = []
        if state.in_edge is None:
            return []
        # Finding previous node
        nodes_connected_to_edge = self.graph.get_endpoints_of_edge(
            state.in_edge)
        previous_node = state.current_node
        for node in nodes_connected_to_edge:
            if node != state.current_node:
                previous_node = node
        # Finding possible previous edges
        if (state.in_edge in self.routing_table[SkippingRoutingState(None, previous_node)]):
            previous_states.append(SkippingRoutingState(None, previous_node))
        for edge in self.graph.get_edges_from_node(previous_node):
            candidate = SkippingRoutingState(edge, previous_node)
            if self.routing_table.get(candidate):
                if state.in_edge in self.routing_table[candidate]:
                    previous_states.append(candidate)
        return previous_states

    def update_routing_table(self, routing_table: dict[SkippingRoutingState, list[int]]) -> None:
        for routing_table_state, routing_table__pref_list in routing_table.items():
            self.check_validity_of_routing_table(
                routing_table_state, self.graph, routing_table__pref_list)
        self.routing_table = routing_table

    def check_validity_of_routing_table(self, state: SkippingRoutingState, graph: Graph, routing_table_of_node: list[int]) -> None:
        if state.in_edge is not None and state.in_edge not in graph.get_edges():
            raise Exception("State in-edge not in Graph")
        if state.current_node not in graph.get_nodes():
            raise Exception("State node not in Graph")
        if (state.in_edge is not None and state.current_node not in graph.get_endpoints_of_edge(state.in_edge)):
            raise Exception("State node not connected to given state in-edge")
        for edge in routing_table_of_node:
            if edge not in graph.get_edges():
                raise Exception("Routing table edge not in Graph")
            if edge not in graph.get_edges_from_node(state.current_node):
                raise Exception(
                    "Routing table edge not connected to state node")


class CombinatorialRouting:
    def get_out_edge(self, state) -> int | None:
        pass

    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass


class Network:
    def __init__(self, graph: Graph, routing_model: RoutingModel) -> None:
        self.graph: Graph = graph
        self.routing_model: RoutingModel = routing_model

    def get_all_paths_to(self, state, visited=[], paths=[]) -> list[list[Any]]:
        if state not in visited:
            direct_previous_states = self.routing_model.get_direct_previous_states(
                state)
            visited.append(state)
            if state.in_edge is None:
                paths.append(visited)
            for direct_previous_state in direct_previous_states:
                self.get_all_paths_to(direct_previous_state, visited, paths)

        return paths 

    # recursive function will end when in-edge is None
    # will have to check for loops, take into account nodes traveled


def main() -> None:
    json_path = "graphs/graph3.json"
    with open(json_path, 'r') as file:
        loaded_graph = json.load(file)

    nodes = loaded_graph["nodes"]
    edge_to_node_mapping = {entry["edge"]: entry["nodes"]
                            for entry in loaded_graph["edge_to_node_mapping"]}

    graph = Graph()
    for node in nodes:
        graph.add_node(node)
    for edge, node_tuple in edge_to_node_mapping.items():
        graph.add_edge(edge, node_tuple[0], node_tuple[1])

    routing_table = {SkippingRoutingState(entry["in_edge"], entry["node"]): entry["out_edges"]
                     for entry in loaded_graph["routing_table"]}

    state = SkippingRoutingState(1, "v1")
    skipping_routing = SkippingRouting(graph)

    skipping_routing.update_routing_table(routing_table)

    print(skipping_routing.get_direct_previous_states(state))

    network = Network(graph, skipping_routing)
    print(network.get_all_paths_to(state))


if __name__ == "__main__":
    main()
