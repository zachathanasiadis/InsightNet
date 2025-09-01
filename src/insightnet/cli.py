from pathlib import Path
import json
import argparse
from .graph_parser import parse_graph
from .routing_model_parser import parse_routing_model
from .network import Network
from .enums import DataFormat
from .export import export_csv, export_json, export_jsonl, export_dot


def main() -> None:
    parser = argparse.ArgumentParser(description="Global insight tool for local routing models")
    parser.add_argument("-i", "--input-json", required=True, type=str,
                        help="Add a JSON file as input containing the following values: routing_model, nodes, edge_to_node_mapping and routing_table")  # TODO
    parser.add_argument("-s", "--current-state", required=True, type=str,
                        help="Add edge and node of the state to be queried, seperated by a comma")
    parser.add_argument("-o", "--output", required=True, type=str,
                        help="Provide destination path and file name with the appropriate extension (.csv/.json/.jsonl/.dot) to export results")
    args = parser.parse_args()

    destination_path = Path(args.output)
    valid_suffixes = {item.value for item in DataFormat}
    if destination_path.suffix not in valid_suffixes:
        raise Exception("Invalid file extension")

    destination_path.parent.mkdir(parents=True, exist_ok=True)

    with open(args.input_json, 'r') as file:
        data = json.load(file)
    graph = parse_graph(data)
    routing_model = parse_routing_model(graph, data)

    network = Network(graph, routing_model)

    state = routing_model.get_state_class().parse_state(args.current_state)

    if destination_path.suffix == DataFormat.DOT.value:
        results = network.get_aggregate_network_results(state)
        export_dot(graph, destination_path, results)
    else:
        results = network.infer_edges_for_every_path_from_given_state(state)
        if destination_path.suffix == DataFormat.CSV.value:
            export_csv(destination_path, results)
        elif destination_path.suffix == DataFormat.JSON.value:
            export_json(destination_path, results)
        elif destination_path.suffix == DataFormat.JSONL.value:
            export_jsonl(destination_path, results)
