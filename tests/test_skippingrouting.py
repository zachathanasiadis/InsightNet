from main import SkippingRouting, SkippingRoutingState, Graph
import pytest


@pytest.fixture
def skipping_routing_instance():
    nodes = ["v0", "v1", "v2"]
    edge_to_node_mapping = {
        1: ["v0", "v1"],
        2: ["v1", "v2"]
    }
    graph = Graph()
    for node in nodes:
        graph.add_node(node)
    for edge, node_tuple in edge_to_node_mapping.items():
        graph.add_edge(edge, node_tuple[0], node_tuple[1])
    skipping_routing = SkippingRouting(graph)
    return skipping_routing


def test_update_routing_table(skipping_routing_instance):
    routing_table = {SkippingRoutingState(1, "v1"): [1]}

    skipping_routing_instance.update_routing_table(routing_table)
    assert skipping_routing_instance.routing_table == routing_table


def test_update_routing_table_state_in_edge_not_in_graph_exception(skipping_routing_instance):
    routing_table = {SkippingRoutingState(3, "v1"): [1]}

    with pytest.raises(Exception, match="State in-edge not in Graph"):
        skipping_routing_instance.update_routing_table(routing_table)


def test_update_routing_table_state_node_not_in_graph_exception(skipping_routing_instance):
    routing_table = {SkippingRoutingState(1, "v3"): [1]}

    with pytest.raises(Exception, match="State node not in Graph"):
        skipping_routing_instance.update_routing_table(routing_table)


def test_update_routing_table_state_node_not_connected_to_given_state_in_edge_exception(skipping_routing_instance):
    routing_table = {SkippingRoutingState(1, "v2"): [1]}

    with pytest.raises(Exception, match="State node not connected to given state in-edge"):
        skipping_routing_instance.update_routing_table(routing_table)


def test_update_routing_table_edge_not_in_graph_exception(skipping_routing_instance):
    routing_table = {SkippingRoutingState(1, "v1"): [1, 3]}

    with pytest.raises(Exception, match="Routing table edge not in Graph"):
        skipping_routing_instance.update_routing_table(routing_table)


def test_update_routing_table_edge_not_connected_to_state_exception(skipping_routing_instance):
    routing_table = {SkippingRoutingState(1, "v0"): [1, 2]}

    with pytest.raises(Exception, match="Routing table edge not connected to state node"):
        skipping_routing_instance.update_routing_table(routing_table)


def test_get_out_edge(skipping_routing_instance):
    routing_table = {SkippingRoutingState(1, "v1"): [1]}

    skipping_routing_instance.update_routing_table(routing_table)
    assert skipping_routing_instance.get_out_edge(
        SkippingRoutingState(1, "v1")) == 1


def test_get_out_edge_returns_None(skipping_routing_instance):
    routing_table = {SkippingRoutingState(1, "v1"): [1]}

    skipping_routing_instance.update_routing_table(routing_table)
    assert skipping_routing_instance.get_out_edge(
        SkippingRoutingState(1, "v1"), [1]) is None


def test_get_direct_previous_states(skipping_routing_instance):
    routing_table = {SkippingRoutingState(None, "v0"): [1],
                     SkippingRoutingState(1, "v0"): [1],
                     SkippingRoutingState(None, "v1"): [1, 2],
                     SkippingRoutingState(1, "v1"): [2, 1],
                     SkippingRoutingState(2, "v1"): [1, 2],
                     SkippingRoutingState(None, "v2"): [2],
                     SkippingRoutingState(2, "v2"): [2],
                     }

    skipping_routing_instance.update_routing_table(routing_table)

    state = SkippingRoutingState(1, "v0")

    assert skipping_routing_instance.get_direct_previous_states(state) == [SkippingRoutingState(
        in_edge=None, current_node='v1'), SkippingRoutingState(in_edge=1, current_node='v1'), SkippingRoutingState(in_edge=2, current_node='v1')]


def test_get_direct_previous_states_returns_empty_list(skipping_routing_instance):
    routing_table = {SkippingRoutingState(None, "v0"): [1],
                     SkippingRoutingState(1, "v0"): [1],
                     SkippingRoutingState(None, "v1"): [1, 2],
                     SkippingRoutingState(1, "v1"): [2, 1],
                     SkippingRoutingState(2, "v1"): [1, 2],
                     SkippingRoutingState(None, "v2"): [2],
                     SkippingRoutingState(2, "v2"): [2],
                     }

    skipping_routing_instance.update_routing_table(routing_table)

    state = SkippingRoutingState(None, "v0")

    assert skipping_routing_instance.get_direct_previous_states(state) == []
