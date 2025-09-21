from typing import Protocol, Any
from .state import State, RequiredEdges, SkippingRoutingState, CombinatorialRoutingState
from .graph import Graph


class RoutingModel(Protocol):
    def get_out_edge(self, state: State, failed_edges: list[int] | None = None) -> int | None:
        raise NotImplementedError

    def get_direct_previous_states(self, state: State) -> list[State]:
        raise NotImplementedError

    def infer_edge_states_from_transition(self, s1: State, s2: State, required_edges: RequiredEdges) -> None:
        raise NotImplementedError

    def get_state_class(self) -> State:
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

    def infer_edge_states_from_transition(self, s1: SkippingRoutingState, s2: SkippingRoutingState, required_edges: RequiredEdges) -> None:
        for edge in self.routing_table[s2]:
            if edge == s1.in_edge:
                required_edges.alive_edges.add(edge)
                break
            else:
                required_edges.failed_edges.add(edge)

    def get_state_class(self) -> State:
        return SkippingRoutingState


class CombinatorialRouting:
    def get_out_edge(self, state: CombinatorialRoutingState) -> int | None:
        pass

    def get_direct_previous_states(self, state: CombinatorialRoutingState) -> list[Any] | None:
        pass

    def update_routing_table(self, routing_table: dict[CombinatorialRoutingState, list[int]]) -> None:
        pass

    def check_validity_of_routing_table(self, routing_table: dict[CombinatorialRoutingState, list[int]]) -> None:
        pass

    def infer_edge_states_from_transition(self, s1: CombinatorialRoutingState, s2: CombinatorialRoutingState) -> None:
        pass
