from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .graph_parser import parse_graph
from .routing_model_parser import parse_routing_model
from .network import Network

app = FastAPI()


class EdgeMapping(BaseModel):
    edge: int
    nodes: list[str]


class RoutingTableEntry(BaseModel):
    in_edge: int | None
    node: str
    out_edges: list[int]


class RoutingRequest(BaseModel):
    routing_model: str
    nodes: list[str]
    edge_to_node_mapping: list[EdgeMapping]
    routing_table: list[RoutingTableEntry]
    current_state: str


@app.post("/infer")
def infer(request: RoutingRequest):
    try:
        data = request.model_dump(exclude={"current_state"})

        graph = parse_graph(data)
        routing_model = parse_routing_model(graph, data)
        network = Network(graph, routing_model)

        current_state = routing_model.get_state_class().parse_state(request.current_state)
        results = []
        for path, result in network.infer_edges_for_every_path_from_given_state(current_state):
            formatted_path = [(state.in_edge, state.current_node) for state in path]
            results.append({"path": formatted_path, "alive_edges": list(
                result.alive_edges), "failed_edges": list(result.failed_edges)})
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=e.args[0])
