from pathlib import Path
from typing import Generator
import json
import csv
import pydot
from .graph import Graph


def export_json(destination_path: Path, results: Generator) -> None:
    try:
        with open(destination_path, "w", newline="") as f:
            f.write('{\n"results": [\n')
            first_entry = True
            for path, result in results:
                if not first_entry:
                    f.write(",\n")
                else:
                    first_entry = False
                formatted_path = [(state.in_edge, state.current_node) for state in path]
                alive_edges = list(result.alive_edges) if result.alive_edges else []
                failed_edges = list(result.failed_edges) if result.failed_edges else []
                res = {"path": formatted_path, "alive_edges": alive_edges, "failed_edges": failed_edges}
                json.dump(res, f)
            f.write("\n]\n}")
    except Exception as e:
        raise Exception(f"Error during JSON export: {e}")


def export_csv(destination_path: Path, results: Generator) -> None:
    try:
        with open(destination_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["path", "alive_edges", "failed_edges"])
            for path, result in results:
                formatted_path = [(state.in_edge, state.current_node) for state in path]
                alive_edges = list(result.alive_edges) if result.alive_edges else []
                failed_edges = list(result.failed_edges) if result.failed_edges else []
                writer.writerow([formatted_path, alive_edges, failed_edges])
    except Exception as e:
        raise Exception(f"Error during CSV export: {e}")


def export_jsonl(destination_path: Path, results: Generator) -> None:
    try:
        with open(destination_path, "w", newline="") as f:
            for path, result in results:
                formatted_path = [(state.in_edge, state.current_node) for state in path]
                alive_edges = list(result.alive_edges) if result.alive_edges else []
                failed_edges = list(result.failed_edges) if result.failed_edges else []
                res = {"path": formatted_path, "alive_edges": alive_edges, "failed_edges": failed_edges}
                f.write(json.dumps(res) + "\n")
    except Exception as e:
        raise Exception(f"Error during JSONL export: {e}")


def export_dot(graph: Graph, destination_path: Path, results: dict[int, dict[str, float]]) -> None:
    dot_graph = pydot.Dot(graph_type="graph")
    dot_graph.set_graph_defaults(rankdir="LR")
    for node in graph.get_nodes():
        dot_graph.add_node(pydot.Node(node))
    for edge, nodes in graph.get_edge_to_node_mapping().items():
        edge_result = results.get(edge, {})
        dominant = max(edge_result.keys(), key=lambda k: edge_result[k])
        color = {"alive_percentage": "green", "failure_percentage": "red", "unknown_percentage": "gray"}.get(dominant, "black")

        dot_graph.add_edge(pydot.Edge(nodes[0], nodes[1], label=str(edge), color=color, fontcolor=color))

    legend = pydot.Subgraph("legend", label="Legend", style="dashed")

    color_legend = """<
    <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
        <TR><TD><FONT COLOR="green">Mostly Alive</FONT></TD></TR>
        <TR><TD><FONT COLOR="red">Mostly Failed</FONT></TD></TR>
        <TR><TD><FONT COLOR="gray">Mostly Unknown</FONT></TD></TR>
    </TABLE>
    >"""

    legend.add_node(pydot.Node("legend_colors", shape="none", label=color_legend))

    dot_graph.add_subgraph(legend)

    dot_graph.write(str(destination_path))
