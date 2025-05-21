def main() -> None:
    def skipping_routing_next_edge(in_edge, out_edges):
        if in_edge != None:
            out_edges.remove(in_edge)
        for out_edge in out_edges:
            if out_edge not in failed_links:
                return out_edge
        return in_edge

    def get_out_edges_for_current_node(in_edge, current_node):
        # implementation without using preference list, resulting in loops 
        # edges = []
        # for edge, node_list in mapping.items():
        #     if current_node in node_list:
        #         edges.append(edge)
        # return edges
        edges = pref_lsit.get(current_node)
        if in_edge != None and edges != None:
            edges.remove(in_edge)
            edges.insert(-1, in_edge)
        return edges
    
    def get_current_node_based_on_incoming_edge(in_edge, current_node):
        for edge, node_list in mapping.items():
            if in_edge == edge:
                for node in node_list:
                    if node != current_node:
                        return node

    def get_path_to(source, destination):
        path = [[None, source]]
        in_edge = None
        current_node = source 
        out_edges = get_out_edges_for_current_node(in_edge,current_node)
        while current_node != destination:
            in_edge = skipping_routing_next_edge(in_edge, out_edges)
            current_node = get_current_node_based_on_incoming_edge(in_edge, current_node)
            out_edges= get_out_edges_for_current_node(in_edge, current_node)
            path.append([in_edge, current_node])
        return path 
    
    # def get_all_paths_to(node):
    #     return

    nodes = ["s", "v1", "v2", "v3", "v4", "d"]
    edges= [0,1,2,3,4,5,6]
    mapping = {
        0 : ["s", "v1"],
        1 : ["s", "v3"],
        2 : ["v1", "v2"],
        3 : ["v3", "v4"],
        4 : ["v2", "v4"],
        5 : ["v2", "d"],
        6 : ["v4", "d"]
    }   
    pref_lsit = {
        "s" : [1, 0],
        "v1" : [2, 0], 
        "v2" : [5, 4, 2],
        "v3" : [3, 1],
        "v4" : [6, 3, 4],
        "d" : [5,6]
    }
    failed_links=[1,5]  

    # alternative representation of the preference list
    # pref_list = {
    #     [None, "s"] : [1, 0],
    #     [1, "s"] : [0, 1],
    #     [0, "s"] : [1, 0],
    #     [None, "v1"] : [2, 0],
    #     [0, "v1"] : [2, 0],
    #     [2, "v1"] : [0, 2], 
    #     [None, "v2"] : [5, 4, 2],
    #     [4, "v2"] : [5, 2, 4],
    #     [2, "v2"] : [5, 4, 2],
    #     [5, "v2"] : [4, 2, 5],
    #     [None, "v3"] : [3, 1],
    #     [1, "v3"] : [3, 1],
    #     [3, "v3"] : [1, 3],
    #     [None, "v4"] : [6, 3, 4],
    #     [4, "v4"] : [6, 3, 4],
    #     [3, "v4"] : [6, 4, 3],
    #     [6, "v4"] : [3, 4, 6],
    #     [None, "d"] : [5, 6],
    #     [6, "d"] : [5, 6],
    #     [5, "d"] : [6, 5]
    # }

    skipping_routing_path = get_path_to("s", "d")
    print(skipping_routing_path)

    #all_paths = get_all_paths_to("d")

if __name__ == "__main__":
    main()
