from itertools import pairwise
from .graph import Graph
from .routing_model import RoutingModel
from .state import State, RequiredEdges
from typing import Generator


class Network:
    def __init__(self, graph: Graph, routing_model: RoutingModel) -> None:
        self.graph: Graph = graph
        self.routing_model: RoutingModel = routing_model

    def get_all_paths_to(self, state) -> Generator[list, None, None]:
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

        return get_all_paths_to_recursive(state)

    def infer_edges_for_every_path_from_given_state(self, state: State) -> Generator[tuple[list, RequiredEdges], None, None]:
        paths = self.get_all_paths_to(state)
        for path in paths:
            required_edges = RequiredEdges()
            for s1, s2 in pairwise(path):
                self.routing_model.infer_edge_states_from_transition(s1, s2, required_edges)
            yield path, required_edges

    def get_aggregate_network_results(self) -> dict[str, dict[str, float]]:
        results = dict()
        for edge in self.graph.edges:
            results[edge] = {"alive_percentage": None, "failure_percentage": None, "unknown_percentage": None}
        return results
