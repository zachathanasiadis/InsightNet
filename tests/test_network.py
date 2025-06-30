from main import Graph, SkippingRouting, SkippingRoutingState, Network
import pytest


@pytest.fixture
def network_sr():
    graph1 = {'routing_model': 'Skipping Routing', 'nodes': ['v1', 'v2', 'v3'], 'edge_to_node_mapping': [{'edge': 1, 'nodes': ['v1', 'v2']}, {'edge': 2, 'nodes': ['v2', 'v3']}], 'routing_table': [{'in_edge': None, 'node': 'v1', 'out_edges': [1]}, {'in_edge': 1, 'node': 'v1', 'out_edges': [
        1]}, {'in_edge': None, 'node': 'v2', 'out_edges': [2, 1]}, {'in_edge': 1, 'node': 'v2', 'out_edges': [2, 1]}, {'in_edge': 2, 'node': 'v2', 'out_edges': [1, 2]}, {'in_edge': None, 'node': 'v3', 'out_edges': [2]}, {'in_edge': 2, 'node': 'v3', 'out_edges': [2]}]}
    nodes = graph1["nodes"]
    edge_to_node_mapping = {entry["edge"]: entry["nodes"] for entry in graph1["edge_to_node_mapping"]}

    graph = Graph()
    for node in nodes:
        graph.add_node(node)
    for edge, endpoints in edge_to_node_mapping.items():
        graph.add_edge(edge, endpoints[0], endpoints[1])
    routing_table = {SkippingRoutingState(entry["in_edge"], entry["node"]): entry["out_edges"]
                     for entry in graph1["routing_table"]}
    skipping_routing = SkippingRouting(graph)
    skipping_routing.update_routing_table(routing_table)
    skipping_routing = SkippingRouting(graph, routing_table)
    n = Network(graph, skipping_routing)
    return n


def test_skipping_routing_get_all_paths_to(network_sr):
    state = SkippingRoutingState(1, "v1")
    paths = network_sr.get_all_paths_to(state)

    expected_result = [[SkippingRoutingState(in_edge=1, current_node='v1'), SkippingRoutingState(in_edge=None, current_node='v2')],
                       [SkippingRoutingState(in_edge=1, current_node='v1'), SkippingRoutingState(in_edge=1, current_node='v2'),
                        SkippingRoutingState(in_edge=None, current_node='v1')],
                       [SkippingRoutingState(in_edge=1, current_node='v1'), SkippingRoutingState(
                           in_edge=2, current_node='v2'), SkippingRoutingState(in_edge=None, current_node='v3')],
                       [SkippingRoutingState(in_edge=1, current_node='v1'), SkippingRoutingState(in_edge=2, current_node='v2'),
                        SkippingRoutingState(in_edge=2, current_node='v3'), SkippingRoutingState(in_edge=None, current_node='v2')],
                       [SkippingRoutingState(in_edge=1, current_node='v1'), SkippingRoutingState(in_edge=2, current_node='v2'),
                        SkippingRoutingState(in_edge=2, current_node='v3'), SkippingRoutingState(
                           in_edge=1, current_node='v2'),
                        SkippingRoutingState(in_edge=None, current_node='v1')]]
    assert paths == expected_result
