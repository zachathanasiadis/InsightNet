from main import Graph
import pytest


# - Consider creating multiple fixtures for other common graphs in other test cases.
@pytest.fixture
def empty_graph():
    graph = Graph()
    return graph


def test_add_node_and_get_nodes(empty_graph):
    empty_graph.add_node("v0")
    assert "v0" in empty_graph.get_nodes()


def test_add_edge_and_get_edges_and_edge_to_node_mapping(empty_graph):
    empty_graph.add_edge(0, "v1", "v2")
    assert empty_graph.get_edge_to_node_mapping()[0] == ("v1", "v2") and 0 in empty_graph.get_edges()


def test_get_edges_from_node(empty_graph):
    empty_graph.add_edge(0, "v0", "v1")
    assert 0 in empty_graph.get_edges_from_node("v0") and 0 in empty_graph.get_edges_from_node("v1")


def test_get_edges_from_node_returns_multiple_edges(empty_graph):
    empty_graph.add_edge(0, "v0", "v1")
    empty_graph.add_edge(1, "v1", "v2")
    expected_edges = set([0, 1])
    assert expected_edges == set(empty_graph.get_edges_from_node("v1"))


def test_get_endpoints_of_edge(empty_graph):
    empty_graph.add_edge(0, "v0", "v1")
    expected_endpoints = set(["v0", "v1"])

    assert expected_endpoints == empty_graph.get_endpoints_of_edge(0)
