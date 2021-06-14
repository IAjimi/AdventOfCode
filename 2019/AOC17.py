class Intcode():
	def __init__(self, program, noun=None, verb=None):
		self.program = {ix:int(val) for ix, val in enumerate(program)}

		if noun:
			self.program[1] = noun
		if verb:
			self.program[2] = verb

		self.i = 0
		self.relative_base = 0
		self._output = []
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
					print('Input needed.')
					self.done = True
					return self
			elif opcode == 4:
				params = [self.parameter_mode(param_mode[0], self.program[self.i + 1])]
				self._output.append(params[0])
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
				self._output.append(self.program[0])
				self.done = True
				return self
			else:
				raise Exception('Unknown opcode.')

			if not ix_change:
				self.i += 1 + len(params)

def get_grid(_input):
	grid = Intcode(_input).run()._output
	grid = ''.join([chr(i) for i in grid]).splitlines()
	grid = grid[:-2]
	return grid

def create_scaffolding(grid):
	'''Creates a list of scaffold locations, finds the robot's position and
	returns the sum for part 1 (scaffold 4-way intersections).

	A bit messy but 2 birds 1 stone: uses the iteration over grid to both create
	scaffold & get part 1.'''
	scaffolding = []
	_sum = 0
	for y in range(len(grid)):
		len_line = len(grid[y])
		for x in range(len_line):
			if grid[y][x] in ['^', '<', '>', 'v']:
				robot_pos = x,y
			elif grid[y][x] == '#':
				scaffolding.append((x, y))
				if x > 1 and y > 1 and x < len_line - 1 and y < len(grid) - 1:
					if grid[y+1][x] == '#' and grid[y-1][x] == '#' and grid[y][x-1] == '#' and grid[y][x+1] == '#':
						alignment_param = x * y
						_sum += alignment_param

	return robot_pos, scaffolding, _sum

def walk_scaffolding(robot_pos, scaffolding):
	''' Walk through whole scaffolding. Always try continuing going in the
	same direction first. Else, try going left or right. If neither option works,
	you've reached the end of the scaffolding.

	Moves are stored in all_moves list. First value is a dummy value after robot moves
	for 1st time.

	:return: list[str]
	'''
	n = 0
	all_moves = []
	x, y = robot_pos
	direction = ''
	prev_move = (0, -1)  # facing up

	while 1:
		left, right = get_left_right(prev_move)

		if (x + prev_move[0], y + prev_move[1]) in scaffolding:
			n += 1
			dx, dy = prev_move[0], prev_move[1]
		elif (x + left[0], y + left[1]) in scaffolding:
			all_moves.append(direction + str(n))
			direction = 'L'
			dx, dy = left[0], left[1]
			n = 1
		elif (x + right[0], y + right[1]) in scaffolding:
			all_moves.append(direction + str(n))
			direction = 'R'
			dx, dy = right[0], right[1]
			n = 1
		else:
			break

		x, y = x + dx, y + dy
		prev_move = dx, dy

	return all_moves[1:]

def get_left_right(move):
	dx, dy = move

	if move in [(0, -1), (0, 1)]:
		left = dy, dx
		right = -dy, -dx
	elif move in [(-1, 0), (1, 0)]:
		left = -dy, -dx
		right = dy, dx
	else:
		raise Exception('Unknown move.')

	return left, right

def translate_to_ascii(seq):
	temp = []

	for string in seq:
		for c in string:
			temp.append(ord(c))
		temp.append(44)  # ascii code for ','

	temp[-1] = 10  # ascii code for newline

	return temp

def collect_dust(_input):
	# Done manually: using all_moves to identify sequences
	main_seq = translate_to_ascii(['A', 'B', 'A', 'B', 'C', 'B', 'C', 'A', 'C', 'C'])
	A = translate_to_ascii(['R', '12', 'L', '10', 'L', '10'])
	B = translate_to_ascii(['L', '6', 'L', '12', 'R', '12', 'L', '4'])
	C = translate_to_ascii(['L', '12', 'R', '12', 'L', '6'])
	video_feed = translate_to_ascii(['y'])  # buggy when using 'n'

	_input[0] = '2'
	computer = Intcode(_input).run()
	for instruction_list in [main_seq, A, B, C, video_feed]:
		# Print output
		clean_output = ''.join([chr(c) for c in computer._output]).splitlines()
		print(clean_output)

		# Run code
		computer = computer.run(instruction_list)

	computer = computer.run(video_feed)
	sol2 = computer._output[-1]  # stops at 99, which returns program[0], but prev value was actual output

	return sol2

if __name__ == '__main__':
	# find way to auto find loops
	_input = open("2019/aoc17.txt").read().rstrip().split(',')
	grid = get_grid(_input)

	robot_pos, scaffolding, sol1 = create_scaffolding(grid)  # 8084
	print(f'PART 1: {sol1}')

	all_moves = walk_scaffolding(robot_pos, scaffolding)
	sol2 = collect_dust(_input)  # 1119775
	print(f'PART 2: {sol2}')


