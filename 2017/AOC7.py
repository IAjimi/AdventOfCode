def parse_input(_input):
    node_graph, value_graph = {}, {}

    for line in _input:
        if '->' in line:
            origin = line.split(' -> ')[0].split(' (')[0]
            dest = line.split(' -> ')[1].split(', ')
        else:
            origin = line.split(' (')[0]
            dest = []

        val = line.split(' (')[1].split(')')[0]

        node_graph[origin] = dest
        value_graph[origin] = int(val)

    return node_graph, value_graph

def visit_nodes(node_graph, value_graph, node):
    val = value_graph[node]
    next_nodes = node_graph[node]

    if next_nodes:
        new_values = []
        for nn in next_nodes:
            new_val = visit_nodes(node_graph, value_graph, nn)
            val += new_val
            new_values.append(new_val)

        if len(set(new_values)) > 1: # unbalanced program
            print(node, next_nodes, new_values)
    else:
        return val

    return val

def main(_input):
    node_graph, value_graph = parse_input(_input)

    # Part 1: Find bottom program
    candidates = list(node_graph.keys())
    destinations = [item for sublist in list(node_graph.values()) for item in sublist]
    bottom_program = [k for k in candidates if k not in destinations][0]

    # Part 2: Find unbalanced program
    ## problem node is arqoys, value is 6 points too high, should be 1853
    v = visit_nodes(node_graph, value_graph, bottom_program) # this prints message

    return bottom_program, v

if __name__ == "__main__":
    _input = open("2017/aoc_7.txt").read().splitlines()
    bottom_program, v = main(_input) # hmvwl, 1853
    print(f"PART 1: {bottom_program} \n PART 2: 1853 (see code)")