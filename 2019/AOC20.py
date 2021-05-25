'''Re-using some of the things I learned doing day 18. A lot of the heavy lifting (including the "recursive" logic)
is done by parsing of the grid (somewhat messy). Finding the shortest path is then (fairly) easy, using
heapq and a "cache" that really just saves the paths that have already been visited.
'''

import heapq
import time

def parse_grid(_input):
	grid, portals = {}, {}

	for y in range(len(_input)):
		for x in range(len(_input[y])):
			if _input[y][x] == ".":
				grid[(x, y)] = _input[y][x]
			elif _input[y][x].isalpha():
				portals[(x, y)] = _input[y][x]

	return grid, portals


def trace_steps(grid, pos, visited=[], destinations={}, steps=0):
	"""This walks through the whole grid to calculate distance
	between keys and starting points. Would be more efficient to iterate
	over letters to take advantage of the fact that distance from a to b = distance from b to a."""
	move = [(-1, 0), (1, 0), (0, 1), (0, -1)]

	while set(visited) != set(grid.keys()):
		val = grid[pos]

		if val.isalpha():
			destinations[val] = steps
		visited.append(pos)

		possible_paths = [(pos[0] + dx, pos[1] + dy) for dx, dy in move]
		possible_paths = [
			p for p in possible_paths if p in grid.keys() and p not in visited
		]

		if not possible_paths:
			return destinations
		elif len(possible_paths) == 1:
			steps += 1
			pos = possible_paths[0]
		else:
			for new_pos in possible_paths:
				destinations = trace_steps(
					grid, new_pos, visited, destinations, steps + 1
				)

	return destinations


def keypath_parsing(grid, portals):
	# part 1 of parsing portals: get locations of each letter in portal name
	assembly_doors = {}
	for pos, letter in portals.items():
		x, y = pos
		for ap in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
			if ap in portals:
				print(letter, ap)
				k = (
					letter + portals[ap]
					if letter < portals[ap]
					else portals[ap] + letter
				)  # ordered name
				if k not in assembly_doors:
					assembly_doors[k] = set([pos, ap])
				else:
					assembly_doors[k].add(pos)
					assembly_doors[k].add(ap)
	print('\n')
	# min_x, max_x, min_y, max_y
	x = [k[0] for k in grid.keys()]
	y = [k[1] for k in grid.keys()]
	min_x, max_x = min(x), max(x)
	min_y, max_y = min(y), max(y)

	# part 2: narrow it down to the part of the portal that leads to an open space
	for k, pos in assembly_doors.items():
		for p in pos:
			x, y = p
			adj_pos = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
			for ap in adj_pos:
				if ap in grid.keys() and grid[ap] == ".":
					# Save to Grid, w/ Outer-Inner distinct
					if (k not in ['AA', 'ZZ']) and (x <= min_x or x >= max_x or y <= min_y or y >= max_y):
						grid[p] = k + 'O'
						print(p, k + 'O')
					else:
						grid[p] = k + 'I' if k not in ['AA', 'ZZ'] else k
						print(p,  k + 'I' if k not in ['AA', 'ZZ'] else k)

	keypaths = {}
	for k, v in grid.items():
		if v.isalpha():
			newpath = trace_steps(grid, k, visited=[], destinations={}, steps=0)
			del newpath[v]  # don't count distance to self
			newpath = {kk: vv - 2 for kk, vv in newpath.items()}
			if v not in ['AA', 'ZZ']:
				matching_portal = v[:2] + 'I' if v[2] == 'O' else v[:2] + 'O'
				newpath[matching_portal] = 1

			if v not in keypaths.keys():
				keypaths[v] = newpath
			else:
				for kk, vv in newpath.items():
					if kk not in keypaths[v]:
						keypaths[v][kk] = vv
					else:
						keypaths[v][kk] = min(vv, keypaths[v][kk])

	return keypaths

def generate_recursive_keypath(keypaths, max_iteration):
	'''VERY gross.


	:param max_iteration: int
	:return: dict
	'''
	recursive_keypath = {}
	for k, kpath in keypaths.items():
		if k in ['AA', 'ZZ']:
			recursive_keypath[k] = {}
			for kk, ksteps in kpath.items():
				if kk in ['AA', 'ZZ']:
					recursive_keypath[k][kk] = ksteps
				elif kk[2] == 'I':
					recursive_keypath[k][kk + '0'] = ksteps

		elif k[2] == 'O':
			for r in range(1, max_iteration+1):
				recursive_keypath[k + str(r)] = {}
				for kk, ksteps in kpath.items():
					if kk not in ['AA', 'ZZ']:
						if kk == k[:2] + 'I':
							recursive_keypath[k + str(r)][kk + str(r - 1)] = ksteps
						else:
							recursive_keypath[k + str(r)][kk + str(r)] = ksteps
		elif k[2] == 'I':
			for r in range(0, max_iteration):
				recursive_keypath[k + str(r)] = {}
				for kk, ksteps in kpath.items():
					if kk not in ['AA', 'ZZ']:
						if kk == k[:2] + 'O':
							recursive_keypath[k + str(r)][kk + str(r + 1)] = ksteps
						elif kk[2] == 'I':
							recursive_keypath[k + str(r)][kk + str(r)] = ksteps
						elif kk[2] == 'O' and r >= 1:
							recursive_keypath[k + str(r)][kk + str(r)] = ksteps
					elif kk in ['AA', 'ZZ'] and r == 0:
						recursive_keypath[k + str(r)][kk] = ksteps

	return recursive_keypath

def shortest_path(keypaths, origin, destination, part=1, recursive_cap=20):
	min_steps = 1000000
	_queue = [(0, origin, [origin])]
	cache = set()

	while len(_queue):
		steps, current_node, path = heapq.heappop(_queue)

		if current_node == destination:
			return min(steps, min_steps)

		possible_paths = [k for k, v in keypaths[current_node].items() if k not in path]
		cachekey = str(steps) + '-' + str(current_node) + '-' + ''.join(set(possible_paths))

		if cachekey not in cache:
			for new_pos in possible_paths:
				if part == 1 or len(new_pos) == 2:
					new_steps = steps + keypaths[current_node][new_pos]
					heapq.heappush(_queue, (new_steps, new_pos, path + [new_pos]))
				elif len(new_pos) > 3 and int(new_pos[3:]) <= recursive_cap:
					new_steps = steps + keypaths[current_node][new_pos]
					heapq.heappush(_queue, (new_steps, new_pos, path + [new_pos]))

				cache.add(cachekey)

	return min_steps


if __name__ == "__main__":
	_input = open("2019/aoc20.txt").read().splitlines()

	t0 = time.time()
	grid, portals = parse_grid(_input)
	keypaths = keypath_parsing(grid, portals)
	min_steps = shortest_path(keypaths, "AA", "ZZ")  # 410
	print(f'min_steps: {min_steps}, speed: {time.time() - t0}') # +-2.3 seconds

	t0 = time.time()
	recursive_keypaths = generate_recursive_keypath(keypaths, 26)
	min_steps = shortest_path(recursive_keypaths, "AA", "ZZ", part=2, recursive_cap=25)  # 5084
	print(f'min_steps: {min_steps}, speed: {time.time() - t0}')  # +-1.8 seconds
