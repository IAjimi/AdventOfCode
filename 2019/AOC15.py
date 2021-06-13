import heapq

class Intcode():
	def __init__(self, program, noun=None, verb=None):
		self.program = {ix:int(val) for ix, val in enumerate(program)}

		if noun:
			self.program[1] = noun
		if verb:
			self.program[2] = verb

		self.i = 0
		self.relative_base = 0
		self._output = None
		self.done = False

	def parameter_mode(self, mode, param):
		if mode == '0':
			return self.program[param]
		elif mode == '1':
			return param
		elif mode == '2':
			return self.program[param + self.relative_base]
		else:
			raise Exception('Invalid mode.')

	def address_mode(self, mode, param):
		if mode == '0':
			return self.program[param]
		elif mode == '1':
			return param
		elif mode == '2':
			return self.program[param] + self.relative_base
		else:
			raise Exception('Invalid mode.')

	def get_params(self, param_mode, n_params):
		params = [None for n in range(n_params)]
		params[0] = self.parameter_mode(param_mode[0], self.program[self.i + 1])
		params[1] = self.parameter_mode(param_mode[1], self.program[self.i + 2])
		if n_params == 3:
			params[2] = self.address_mode(param_mode[2], self.i + 3)
		return params

	def run(self, _input=[]):
		while self.i <= len(self.program):
			self.done = False
			instruction = self.program[self.i]
			opcode = instruction % 100
			param_mode = str(instruction // 100)
			param_mode = param_mode[::-1] + '0' * (3 - len(param_mode))
			ix_change = False

			if opcode == 1:
				params = self.get_params(param_mode, 3)
				self.program[params[2]] = params[0] + params[1]
			elif opcode == 2:
				params = self.get_params(param_mode, 3)
				self.program[params[2]] = params[0] * params[1]
			elif opcode == 3:
				if _input:
					params = [self.address_mode(param_mode[0], self.i + 1)]
					current_input = _input[0]
					_input.pop(0)
					self.program[params[0]] = current_input
				else:
					self.done = True
					return self
			elif opcode == 4:
				params = [self.parameter_mode(param_mode[0], self.program[self.i + 1])]
				self._output = params[0]
				#self.i += 1 + len(params)
				#return self
			elif opcode == 5:
				params = self.get_params(param_mode, 2)
				if params[0] != 0:
					self.i = params[1]
					ix_change = True
			elif opcode == 6:
				params = self.get_params(param_mode, 2)
				if params[0] == 0:
					self.i = params[1]
					ix_change = True
			elif opcode == 7:
				params = self.get_params(param_mode, 3)
				self.program[params[2]] = 1 if params[0] < params[1] else 0
			elif opcode == 8:
				params = self.get_params(param_mode, 3)
				self.program[params[2]] = 1 if params[0] == params[1] else 0
			elif opcode == 9:
				params = [self.parameter_mode(param_mode[0], self.program[self.i + 1])]
				self.relative_base += params[0]
			elif opcode == 99:
				self._output = self.program[0]
				self.done = True
				return self
			else:
				raise Exception('Unknown opcode.')

			if not ix_change:
				self.i += 1 + len(params)



def walk_grid(_input, origin):
	'''Both yields a full scan of the terrain and finds the shortest path
	to the oxygen.'''
	grid = {}
	min_steps = 10000
	_queue = [(0, origin, [])]

	while len(_queue):
		steps, current_cell, moves = heapq.heappop(_queue)
		x, y = current_cell

		if current_cell != origin:
			intcode = Intcode(_input).run(moves.copy())
			new_val = intcode._output  # last output value
		else:
			new_val = 1

		grid[(x, y)] = new_val

		if new_val == 2:
			min_steps = steps

		if new_val in [1, 2]:
			possible_paths = [(1, (x, y + 1)), (2, (x, y - 1)), (3, (x - 1, y)), (4, (x + 1, y))]  # move, position
			possible_paths = [p for p in possible_paths if p[1] not in grid.keys()]

			for new_move, new_pos in possible_paths:
				heapq.heappush(_queue, (steps + 1, new_pos, moves + [new_move]))

	return min_steps, grid

def max_steps(grid, origin):
	_queue = [(0, origin, [origin])]

	while len(_queue):
		steps, current_cell, path = heapq.heappop(_queue)
		x, y = current_cell

		possible_paths = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
		possible_paths = [p for p in possible_paths if p in grid.keys() and p not in path]

		for new_pos in possible_paths:
			heapq.heappush(_queue, (steps + 1, new_pos, path + [new_pos]))

	return steps  # will be max at the end of the queue


if __name__ == '__main__':
	# change to regular queue since steps = 1
	# https://docs.python.org/3/library/queue.html
	_input = open("2019/aoc15.txt").read().rstrip().split(',')
	sol1, grid = walk_grid(_input, (0, 0))  # 242
	print(f'PART 1: {sol1}')

	open_spaces = {k:v for k,v in grid.items() if v != 0}
	oxygen_loc = [k for k,v in grid.items() if v == 2][0]
	steps = max_steps(open_spaces, oxygen_loc)  # 276

