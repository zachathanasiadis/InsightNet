from .routing_model import SkippingRouting
from .state import SkippingRoutingState
from .graph import Graph
from typing import Any

model_parsers = dict()


def parse_routing_model(graph: Graph, data: dict[str, Any]):
    if data["routing_model"] not in model_parsers:
        raise KeyError(f"Routing model named {data["routing_model"]} is invalid")
    try:
        return model_parsers[data["routing_model"]](graph, data)
    except Exception as e:
        raise e


def register_model_parser(routing_model: str):
    def wrapper(func):
        model_parsers[routing_model] = func
        return func
    return wrapper


@register_model_parser(routing_model="Skipping Routing")
def parse_skipping_routing(graph: Graph, data: dict[str, Any]) -> SkippingRouting:
    routing_table = {SkippingRoutingState(entry["in_edge"], entry["node"]): entry["out_edges"] for entry in data["routing_table"]}
    skipping_routing = SkippingRouting(graph)
    skipping_routing.update_routing_table(routing_table)
    return skipping_routing