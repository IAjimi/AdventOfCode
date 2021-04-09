def char_position(arg):
    return ord(arg.lower()) - 97

def add_to_dict(key, val, d):
	# """Helps generate the dictionaries in process_input."""
    if key not in d.keys():
        d[key] = [val]
    else:
        d[key].append(val)

    return d

def process_input(_input):
	# """ This has a 'forward_path' because I initially understood the problem as having to
	# be at a node to move forward to next nodes. It is still here because it helps find the
	# nodes without any requirements (possible_start_nodes), though having a set of all nodes could do the same
	# thing, and the end node."""
    forward_path = {}
    requirements = {}

    for i in _input:
        _from = i.split('Step ')[1].split(' ')[0]
        _to = i.split('before step ')[1].split(' can')[0]

        add_to_dict(_from, _to, forward_path)
        add_to_dict(_to, _from, requirements)

    end_node = list(set(requirements.keys()).difference(set(forward_path.keys())))[0]
    possible_start_nodes = list(set(forward_path.keys()).difference(set(requirements.keys())))

    # Adding possible start notes to backward path
    for p in possible_start_nodes: requirements[p] = []

    return end_node, requirements

def traverse_path(end_node, requirements, n_workers):
    workers = {str(r):None for r in range(n_workers)}
    progress_node = []
    path = []
    t = 0

    while end_node not in path:
        # Find paths
        possible_paths = [k for k,v in requirements.items() if v == [] and k not in progress_node and k not in path]

        # Allocate nodes to workers
        for w,task in workers.items():
            busy = True if task else False

            if busy:
                # Check if task completed, if so update things accordingly
                if t >= task[1]:
                    node = task[0]
                    workers[w] = None

                    path.append(node)
                    progress_node.remove(node)

                    for p in requirements.keys():
                        if node in requirements[p]:
                            requirements[p].remove(node)

                    busy = False

            if not busy:
                updated_possible_paths = [v for v in possible_paths if v not in progress_node]

                if updated_possible_paths:
                    node = min(updated_possible_paths)
                    workers[w] = (node, 60 + t + char_position(node))
                    progress_node.append(node)

        t += 1

    return ''.join(path), t

if __name__ == "__main__":
	_input = open("aoc_7.txt").read().splitlines()

	print("PART 1")
	end_node, requirements = process_input(_input)
	print(traverse_path(end_node, requirements, 1)) # JKNSTHCBGRVDXWAYFOQLMPZIUE

	print("PART 2")
	end_node, requirements = process_input(_input)
	print(traverse_path(end_node, requirements, 5)) # 'JNSVKDYTXHRCGBOWAFQLMPZIUE', 755