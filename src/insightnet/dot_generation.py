from .graph import Graph
import pydot


def generate_dot_file(graph: Graph) -> None:
    dot_graph = pydot.Dot(graph_type="graph")
    dot_graph.set_graph_defaults(rankdir="LR")
    for node in graph.get_nodes():
        dot_graph.add_node(pydot.Node(node))
    for edge, nodes in graph.get_edge_to_node_mapping().items():
        dot_graph.add_edge(pydot.Edge(nodes[0], nodes[1], label=edge))
    dot_graph.write("graph.dot")
