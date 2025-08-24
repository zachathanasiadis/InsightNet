from pathlib import Path
import json
import argparse
from .graph_parser import parse_graph
from .routing_model_parser import parse_routing_model
from .network import Network
from .enums import DataFormat
from .export import export_csv, export_json, export_jsonl
from .dot_generation import generate_dot_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Global insight tool for local routing models")
    parser.add_argument("-i", "--input-json", required=True, type=str,
                        help="Add a JSON file as input containing the following values: routing_model, nodes, edge_to_node_mapping and routing_table")  # TODO
    parser.add_argument("-s", "--current-state", required=True, type=str,
                        help="Add edge and node of the state to be queried, seperated by a comma")
    parser.add_argument("-o", "--output", required=True, type=str,
                        help="Provide destination path and file name with the appropriate extension (.csv/.json/.jsonl) to export results")
    parser.add_argument("-d", "--dot", action='store_true', help="Export graph in DOT format.")
    args = parser.parse_args()
    with open(args.input_json, 'r') as file:
        data = json.load(file)
    graph = parse_graph(data)
    routing_model = parse_routing_model(graph, data)

    network = Network(graph, routing_model)

    state = routing_model.get_state_class().parse_state(args.current_state)

    results = network.infer_edges_for_every_path_from_given_state(state)

    destination_path = Path(args.output)

    destination_path.parent.mkdir(parents=True, exist_ok=True)

    if destination_path.suffix == DataFormat.CSV.value:
        export_csv(destination_path, results)
    elif destination_path.suffix == DataFormat.JSON.value:
        export_json(destination_path, results)
    elif destination_path.suffix == DataFormat.JSONL.value:
        export_jsonl(destination_path, results)
    else:
        raise Exception("Invalid file extension")

    if args.dot:
        generate_dot_file(graph)