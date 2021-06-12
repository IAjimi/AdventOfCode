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
				self.i += 1 + len(params)
				return self
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

class ArcadeCabinet():
	def __init__(self, program):
		self.program = program
		self._input = []
		self.screen = {}
		self.score = 0
		self.paddle = None
		self.ball = None

	def parse_output(self, x, y, tile):
		if x == -1 and y == 0:
			self.score = tile
			print(f'SCORE: {tile}')
		elif tile == 0:
			self.screen[(x,y)] = ' '
		elif tile == 1:
			self.screen[(x,y)] = chr(9608)
		elif tile == 2:
			self.screen[(x,y)] = '.'
		elif tile == 3:
			self.screen[(x,y)] = '_'
			self.paddle = x, y
		elif tile == 4:
			if self.ball in self.screen:
				self.screen[self.ball] = ' '

			self.screen[(x,y)] = 'o'
			self.ball = x, y
		else:
			raise Exception('Unknown tile id.')

	def __str__(self):
		str_rep = ''
		for y in range(0, 25):
			line = []
			for x in range(0, 41):
				line.append(self.screen[x, y])

			str_rep += ''.join(line)
			str_rep += '\n'

		return str_rep

	def run(self, part=1):
		if part == 1:
			intcode = Intcode(self.program).run(_input=[])
			self._input.append(intcode._output)

			while not intcode.done:
				intcode = intcode.run()
				self._input.append(intcode._output)

			for r in range(0, len(self._input) - 3, 3):
				x, y ,tile = self._input[r], self._input[r+1], self._input[r+2]
				self.parse_output(x, y, tile)

		elif part == 2:
			self.program[0] = '2'
			intcode = Intcode(self.program)
			joystick = []
			done = False

			while not done:
				x = intcode.run(joystick)._output
				if joystick:
					joystick.pop(0)
				y = intcode.run(joystick)._output
				tile = intcode.run(joystick)._output
				self.parse_output(x, y, tile)

				if self.ball and self.paddle:
					if self.ball[0] - self.paddle[0] < 0:  # ball is left of paddle
						joystick.append(-1)
					elif self.ball[0] - self.paddle[0] > 0:  # ball is right of paddle
						joystick.append(1)
					else:
						joystick.append(0)

					if sum([1 for v in self.screen.values() if v == '.']) == 0:
						x = intcode.run()._output
						y = intcode.run()._output
						tile = intcode.run()._output
						self.parse_output(x, y, tile)
						done = True

		return self



if __name__ == '__main__':
	_input = open("2019/aoc13.txt").read().rstrip().split(',')
	arcade = ArcadeCabinet(_input).run()
	sol1 = sum([1 for k, v in arcade.screen.items() if v == '.'])
	print(f'PART 1: {sol1}')

	sol2 = ArcadeCabinet(_input).run(part=2) # 18647
	print(f'PART 2: {sol2.score}')