from typing import Any, Protocol
from dataclasses import dataclass, field
from itertools import pairwise
import json
import argparse


@dataclass(frozen=True)
class SkippingRoutingState:
    in_edge: int | None
    current_node: str


class CombinatorialRoutingState:
    pass


@dataclass(frozen=True)
class RequiredEdges:
    alive_edges: set[int] = field(default_factory=set)
    failed_edges: set[int] = field(default_factory=set)


class Graph:
    def __init__(self, nodes: list[str] | None = None, edges: list[int] | None = None, edge_to_node_mapping: dict[int, tuple[str, str]] | None = None) -> None:
        self.nodes: list[str] = nodes if nodes is not None else []
        self.edges: list[int] = edges if edges is not None else []
        self.edge_to_node_mapping: dict[int, tuple[str, str]] = edge_to_node_mapping if edge_to_node_mapping is not None else {}

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

    # TODO add type annotations
    def infer_edge_states_from_transition(self, s1, s2, required_edges):
        raise NotImplementedError


class SkippingRouting:
    def __init__(self, graph: Graph, routing_table: dict[SkippingRoutingState, list[int]] | None = None) -> None:
        self.graph: Graph = graph
        if routing_table is not None:
            self.check_validity_of_routing_table(routing_table)
        self.routing_table: dict[SkippingRoutingState, list[int]] = routing_table if routing_table is not None else {}

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
                raise Exception("Routing table edge not connected to state node")

    def infer_edge_states_from_transition(self, s1: SkippingRoutingState, s2: SkippingRoutingState, required_edges: RequiredEdges):
        for edge in self.routing_table[s2]:
            if edge == s1.in_edge:
                required_edges.alive_edges.add(edge)
                break
            else:
                required_edges.failed_edges.add(edge)


class CombinatorialRouting:
    def get_out_edge(self, state) -> int | None:
        pass

    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass

    def update_routing_table(self, routing_table: dict[CombinatorialRoutingState, list[int]]) -> None:
        pass

    def check_validity_of_routing_table(self, routing_table: dict[CombinatorialRoutingState, list[int]]) -> None:
        pass

    def infer_edge_states_from_transition(self, s1: CombinatorialRoutingState, s2: CombinatorialRoutingState):
        pass


class Network:
    def __init__(self, graph: Graph, routing_model: RoutingModel) -> None:
        self.graph: Graph = graph
        self.routing_model: RoutingModel = routing_model

    def get_all_paths_to(self, state) -> list[list[Any]]:
        def get_all_paths_to_recursive(state, path=None):
            if path is None:
                path = []
            if state in path:
                return

            path = path + [state]
            if state.in_edge is None:
                yield path
                return

            for direct_previous_state in self.routing_model.get_direct_previous_states(state):
                yield from get_all_paths_to_recursive(direct_previous_state, path)

        return list(get_all_paths_to_recursive(state))

    def infer_edges_for_every_path_from_given_state(self, state: SkippingRoutingState):
        paths = self.get_all_paths_to(state)
        for path in paths:
            required_edges = RequiredEdges()
            for s1, s2 in pairwise(path):
                self.routing_model.infer_edge_states_from_transition(s1, s2, required_edges)
            yield required_edges


model_parsers = dict()


def register_model_parser(routing_model: str):
    def wrapper(func):
        model_parsers[routing_model] = func
        return func
    return wrapper


@register_model_parser(routing_model="Skipping Routing")
def parse_skipping_routing(graph: Graph, data: dict[str, Any]) -> SkippingRouting:
    routing_table = {SkippingRoutingState(entry["in_edge"], entry["node"]): entry["out_edges"] for entry in data["routing_table"]}
    skipping_routing = SkippingRouting(graph)
    skipping_routing.update_routing_table(routing_table)
    return skipping_routing


def parse_routing_model(graph: Graph, data: dict[str, Any]):
    try:
        return model_parsers[data["routing_model"]](graph, data)
    except Exception as e:
        raise KeyError(f"Routing model named {e} is invalid")


def parse_graph(data: dict[str, Any]):
    graph = Graph()
    for node in data["nodes"]:
        graph.add_node(node)
    for entry in data["edge_to_node_mapping"]:
        graph.add_edge(entry["edge"], entry["nodes"][0], entry["nodes"][1])
    return graph


def main() -> None:
    parser = argparse.ArgumentParser(description="Global insight tool for local routing models")
    parser.add_argument("-i", "--input-json", required=True, type=str, help="Add a JSON file as input")
    parser.add_argument("-e", "--in-edge", required=True, type=int, help="Add in-edge of the state")
    parser.add_argument("-n", "--current-node", required=True, type=str, help="Add current node of the state")
    args = parser.parse_args()
    with open(args.input_json, 'r') as file:
        data = json.load(file)
    graph = parse_graph(data)
    routing_model = parse_routing_model(graph, data)

    network = Network(graph, routing_model)

    state = SkippingRoutingState(args.in_edge, args.current_node)
    print(*network.infer_edges_for_every_path_from_given_state(state))


if __name__ == "__main__":
    main()
