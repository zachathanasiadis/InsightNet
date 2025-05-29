# Note: Hmmm... How can a test avoid importing the method/class/module/... ?
def main() -> None:
    def skipping_routing_next_edge(out_edges):
        for node in out_edges:
            if is_edge_in_preference_list(node):
                return node
        return None

    def is_edge_in_preference_list(node):
        for tuple_key in pref_list:
            if node in tuple_key:
                return True
        return False

    def get_out_edges_for_current_node(in_edge, current_node):
        edges = pref_list.get((in_edge,current_node))
        return edges

    def get_current_node_based_on_incoming_edge(in_edge, previous_node):
        nodes = edge_to_node_mapping.get(in_edge)
        if nodes !=None:
            for node in nodes:
                if node != previous_node:
                    return  node
        return None

    def get_path_to(source, destination):
        # Note: what happens if the packet can not be delivered?
        # Note: why is this function neccessary?
        path = [[None, source]]
        in_edge = None
        current_node = source
        out_edges = get_out_edges_for_current_node(in_edge,current_node)
        while current_node != destination:
            in_edge = skipping_routing_next_edge(out_edges)
            current_node = get_current_node_based_on_incoming_edge(in_edge, current_node)
            out_edges= get_out_edges_for_current_node(in_edge, current_node)
            path.append([in_edge, current_node])
        return path

    # def get_direct_previous_node():
    #     return

    # def get_all_paths_to(node):
    #     paths = []
    #     previous_node= get_direct_previous_node()

    #     return []

    nodes = ["s", "v1", "v2", "v3", "v4", "d"]
    edges= [0,1,2,3,4,5,6]

    edge_to_node_mapping = {
        0 : ["s", "v1"],
        1 : ["s", "v3"],
        2 : ["v1", "v2"],
        3 : ["v3", "v4"],
        4 : ["v2", "v4"],
        5 : ["v2", "d"],
        6 : ["v4", "d"]
    }
 
    # alternative representation of the preference list
    pref_list = {
        (None, "s") : [1, 0],
        #(1, "s") : [0, 1],
        (0, "s") : [1, 0],
        (None, "v1") : [2, 0],
        (0, "v1") : [2, 0],
        (2, "v1") : [0, 2],
        (None, "v2") : [5, 4, 2],
        (4, "v2") : [5, 2, 4],
        (2, "v2") : [5, 4, 2],
        #(5, "v2") : [4, 2, 5],
        (None, "v3") : [3, 1],
        #(1, "v3") : [3, 1],
        (3, "v3") : [1, 3],
        (None, "v4") : [6, 3, 4],
        (4, "v4") : [6, 3, 4],
        (3, "v4") : [6, 4, 3],
        (6, "v4") : [3, 4, 6],
        (None, "d") : [5, 6],
        (6, "d") : [5, 6]
        #(5, "d") : [6, 5]
    }

    skipping_routing_path = get_path_to("s", "d")
    print(skipping_routing_path)

    # all_paths = get_all_paths_to("d")
    # print(all_paths)

if __name__ == "__main__":
    main()
