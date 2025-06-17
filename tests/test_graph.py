from main import Graph
import pytest


@pytest.fixture
def graph_instance():
    graph = Graph()
    return graph


def test_add_node_and_get_nodes(graph_instance):
    graph_instance.add_node("v0")
    assert "v0" in graph_instance.get_nodes()


def test_add_edge_and_get_edges_and_edge_to_node_mapping(graph_instance):
    graph_instance.add_edge(0, "v1", "v2")
    assert graph_instance.edge_to_node_mapping[0] == ("v1", "v2") and 0 in graph_instance.get_edges()


def test_get_edges_from_node(graph_instance):
    graph_instance.add_edge(0, "v0", "v1")
    assert 0 in graph_instance.get_edges_from_node(
        "v0") and 0 in graph_instance.get_edges_from_node("v1")


def test_get_endpoints_of_edge(graph_instance):
    graph_instance.add_edge(0, "v0", "v1")
    assert "v0" in graph_instance.get_endpoints_of_edge(
        0) or "v1" in graph_instance.get_endpoints_of_edge(0)
