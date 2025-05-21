from typing import Any, Protocol

class RoutingModel(Protocol):
    def get_out_edge(self, state): 
        pass 

    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass

class SkippingRoutingState:
    def __init__(self, in_edge: int, current_node: str, out_edges: list[int]) -> None:
        self.in_edge = in_edge
        self.current_node = current_node
        self.out_edges = out_edges

class SkippingRouting:
    def get_out_edge(self, state: SkippingRoutingState): 
        pass 
    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass

class CombinatorialRoutingState:
    pass
    
class CombinatorialRouting:   
    def get_out_edge(self, state): 
        pass 
    def get_direct_previous_states(self, state) -> list[Any] | None:
        pass

class Graph:
    def __init__(self, nodes: list[str], edges: list[int], mapping: dict[int, tuple[str, str]], failed_links: list[int]) -> None:
        self.nodes = nodes
        self.edges = edges 
        self.mapping = mapping
        self.failed_links = failed_links

    def get_nodes(self) -> list[str]:
        return self.nodes
    
    def get_edges(self) -> list[int]:
        return self.edges

    def get_mapping(self) -> dict[int, tuple[str, str]]:
        return self.mapping
    
class Network:
    def __init__(self, graph: Graph, routing_model: RoutingModel) -> None:
        self.graph: Graph = graph
        self.routing_model: RoutingModel = routing_model

    def get_all_paths_to(self, state) -> list[list[Any]] | None:
        pass    
    
    def get_path_to(self, source: SkippingRoutingState, destination: SkippingRoutingState):
        pass 
    
def main() -> None:

    def skipping_routing_next_edge(in_edge, current_node, out_edges):
        if failed_links not in out_edges:
            pass 

    def get_out_edges_for(node):
        pass 
    
    def get_path_to(source, destination):
        path = []
        in_edge = None
        current_node = source 
        out_edges = get_out_edges_for(current_node)
        while current_node != destination:
            skipping_routing_next_edge(in_edge, current_node, out_edges)

    nodes = ["s", "v1", "v2", "v3", "v4", "d"]
    edges= [0,1,2,3,4,5,6]
    mapping = {
        0 : ("s", "v1"),
        1 : ("s", "v3"),
        2 : ("v1", "v2"),
        3 : ("v3", "v4"),
        4 : ("v2", "v4"),
        5 : ("v2", "d"),
        6 : ("v4", "d")
    }

    failed_links=[1,5]
   
    skipping_routing_path = get_path_to("s","d")


    routing_model: RoutingModel = SkippingRouting()
    graph = Graph(nodes, edges, mapping, failed_links)
    network = Network(graph, routing_model)

if __name__ == "__main__":
    main()
