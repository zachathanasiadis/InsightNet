class Node:
    def __init__(self, nodeName: str, adjacencyList: list) -> None:
        self.nodeName = nodeName 
        self.adjacencyList = adjacencyList
        self.preferenceList = []
        self.possiblePaths = []
        self.routingModel = "Skipping" 

    def getPossiblePaths(self) -> list[list[str]]:
        # Implement DFS(?) to find all possible paths leading to queried node
        # Output: A list of lists, representing the possbile paths
        pass 
    
    def getAliveAndFailedEdges(self):
        if self.routingModel == "Skipping":
            pass
        elif self.routingModel == "Combinatorial":
            pass

    def __str__(self) -> str:
        return f"Node: {self.nodeName} - Adjacenct Nodes: {self.adjacencyList}"

def main() -> None:
    graph = {
    "s" : ["v1", "v2"],
    "v1" : ["s", "v2"],
    "v2" : ["v1", "v4", "d"],
    "v3" : ["s", "v4"],
    "v4" : ["v2", "v3", "d"],
    "d" : ["v2", "v4"]
    }
    for i in graph:
        node = Node(i, graph[i])
        print(node)

if __name__ == "__main__":
    main()
