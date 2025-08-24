from pathlib import Path
from typing import Generator
import json
import csv


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
