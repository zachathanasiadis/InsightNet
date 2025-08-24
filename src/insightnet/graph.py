class Graph:
    def __init__(self, nodes: list[str] | None = None, edges: list[int] | None = None, edge_to_node_mapping: dict[int, tuple[str, str]] | None = None) -> None:
        self.nodes: list[str] = nodes if nodes is not None else []
        self.edges: list[int] = edges if edges is not None else []
        self.edge_to_node_mapping: dict[int, tuple[str, str]] = edge_to_node_mapping if edge_to_node_mapping is not None else {}

    def get_nodes(self) -> list[str]:
        return self.nodes

    def get_edges(self) -> list[int]:
        return self.edges

    def get_edge_to_node_mapping(self) -> dict[int, tuple[str, str]]:
        return self.edge_to_node_mapping

    def get_edges_from_node(self, node: str) -> list[int]:
        return [edge for edge, node_tuple in self.edge_to_node_mapping.items() if node in node_tuple]

    def get_endpoints_of_edge(self, edge: int) -> set[str]:
        return set(self.edge_to_node_mapping[edge])

    def add_node(self, node: str) -> None:
        self.nodes.append(node)

    def add_edge(self, edge_id: int, v1: str, v2: str) -> None:
        self.edge_to_node_mapping[edge_id] = (v1, v2)
        self.edges.append(edge_id)
