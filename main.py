from typing import Any, Protocol
from dataclasses import dataclass
import json
import argparse


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

    def infer_edge_states_from_transition(self, s1, s2):
        pass


class SkippingRouting:
    def __init__(self, graph: Graph, routing_table: dict[SkippingRoutingState, list[int]] = {}) -> None:
        self.graph = graph
        self.check_validity_of_routing_table(routing_table)
        self.routing_table: dict[SkippingRoutingState, list[int]] = routing_table

    def get_out_edge(self, state: SkippingRoutingState, failed_edges: list[int] | None = None) -> int | None:
        if failed_edges is None:
            failed_edges = []
        for edge in self.routing_table[state]:
            if edge not in failed_edges:
                return edge
        return None

    def get_direct_previous_states(self, state: SkippingRoutingState) -> list[SkippingRoutingState]:
        previous_states = []
        nodes_connected_to_edge = []
        if state.in_edge is None:
            return []
        # Finding previous node
        nodes_connected_to_edge = self.graph.get_endpoints_of_edge(state.in_edge)
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
        self.check_validity_of_routing_table(routing_table)
        self.routing_table = routing_table

    def check_validity_of_routing_table(self, routing_table: dict[SkippingRoutingState, list[int]]) -> None:
        for state, pref_list in routing_table.items():
            self.check_validity_of_routing_table_entry(state, self.graph, pref_list)

    def check_validity_of_routing_table_entry(self, state: SkippingRoutingState, graph: Graph, pref_list: list[int]) -> None:
        if state.in_edge is not None and state.in_edge not in graph.get_edges():
            raise Exception("State in-edge not in Graph")
        if state.current_node not in graph.get_nodes():
            raise Exception("State node not in Graph")
        if (state.in_edge is not None and state.current_node not in graph.get_endpoints_of_edge(state.in_edge)):
            raise Exception("State node not connected to given state in-edge")
        for edge in pref_list:
            if edge not in graph.get_edges():
                raise Exception("Routing table edge not in Graph")
            if edge not in graph.get_edges_from_node(state.current_node):
                raise Exception(
                    "Routing table edge not connected to state node")

    def infer_edge_states_from_transition(self, s1: SkippingRoutingState, s2: SkippingRoutingState):
        pass


class CombinatorialRouting:
    def get_out_edge(self, state) -> int | None:
        pass

    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass

    def update_routing_table(self, routing_table: dict[SkippingRoutingState, list[int]]) -> None:
        pass

    def check_validity_of_routing_table(self, routing_table: dict[CombinatorialRoutingState, list[int]]) -> None:
        pass

    def infer_edge_states_from_transition(self, s1: CombinatorialRoutingState, s2: CombinatorialRoutingState):
        pass


class Network:
    def __init__(self, graph: Graph, routing_model: RoutingModel) -> None:
        self.graph: Graph = graph
        self.routing_model: RoutingModel = routing_model

    def get_all_paths_to(self, state) -> list[list[Any]]:  # Look into yield
        paths = []

        def get_all_paths_to_recursive(state, path=None):
            if path is None:
                path = []
            if state in path:
                return

            path = path + [state]
            if state.in_edge is None:
                paths.append(path)
                return

            direct_previous_states = self.routing_model.get_direct_previous_states(
                state)
            for direct_previous_state in direct_previous_states:
                get_all_paths_to_recursive(direct_previous_state, path)

        get_all_paths_to_recursive(state)
        return paths

    def infer_edges_for_every_path_from_given_state(self, state: SkippingRoutingState):
        paths = self.get_all_paths_to(state)
        for path in paths:
            required_alive_edges = []
            required_failed_edges = []
            for i in range(len(path)-1):
                s1 = path[i]
                s2 = path[i+1]
                self.routing_model.infer_edge_states_from_transition(s1, s2)

        return
# create a function in the skippping routing class called infer_edge_states_from_transition ( two state inputs)
#  -> required alive edges and required failed edges
# create a function in the network class that will take the paths as input and for every scenario aggregate
# required alive and failed edges


def parse_json(json_path: str):
    with open(json_path, 'r') as file:
        loaded_graph = json.load(file)

    nodes = loaded_graph["nodes"]
    edge_to_node_mapping = {entry["edge"]: entry["nodes"] for entry in loaded_graph["edge_to_node_mapping"]}

    graph = Graph()
    for node in nodes:
        graph.add_node(node)
    for edge, endpoints in edge_to_node_mapping.items():
        graph.add_edge(edge, endpoints[0], endpoints[1])

    if loaded_graph["routing_model"] == "Skipping Routing":
        routing_table = {SkippingRoutingState(entry["in_edge"], entry["node"]): entry["out_edges"]
                         for entry in loaded_graph["routing_table"]}

        skipping_routing = SkippingRouting(graph)
        skipping_routing.update_routing_table(routing_table)

        network = Network(graph, skipping_routing)
        return graph, skipping_routing, network
    raise Exception("Invalid Routing Model")


def main() -> None:
    # - Very good start.
    # - Create a helper function that gets a file name and returns the Network, Graph and RoutingModel objects.
    # - Be careful with the design. How will you support JSON parsing when youhave multiple possible routing models implemented?
    parser = argparse.ArgumentParser(description="Global insight tool for local routing models")
    parser.add_argument("-i", "--input", nargs=1, required=True, type=str, help="Add a JSON file as input")
    args = parser.parse_args()
    json_path = args.input[0]
    graph, skipping_routing, network = parse_json(json_path)

    state = SkippingRoutingState(1, "v1")
    paths = network.get_all_paths_to(state)
    print(paths)


if __name__ == "__main__":
    main()
