def travel_path(node, graph, visited = set()):
    visited.add(node)
    next_nodes = graph[node]

    for nn in next_nodes:
        if nn not in visited:
            new_visits = travel_path(nn, graph, visited)
            for nv in new_visits: visited.add(nv)

    return visited

def find_all_paths(graph, visited):
    all_nodes = set(graph.keys())
    not_visited = all_nodes.difference(visited)
    n = 1 # number of unique sets of nodes

    while not_visited:
        n += 1
        random_node = list(not_visited)[0]
        new_visited = travel_path(random_node, graph)
        visited = visited.union(new_visited)
        not_visited = all_nodes.difference(visited)

    return n

if __name__ == "__main__":
    _input = open("2017/aoc_12.txt").read().splitlines()
    _input = [i.split(' <-> ') for i in _input]
    graph = {key: val.split(', ') for key, val in _input}

    visited = travel_path('0', graph)
    sol1 = len(visited)  # 288
    sol2 = find_all_paths(graph, visited) # 211

    print(f"PART 1: {sol1} \n PART 2: {sol2}")