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
				params = [self.address_mode(param_mode[0], self.i + 1)]
				current_input = _input[0]
				_input.pop(0)
				self.program[params[0]] = current_input
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
				return self
			else:
				raise Exception('Unknown opcode.')

			if not ix_change:
				self.i += 1 + len(params)


if __name__ == '__main__':
	_input = open("2019/aoc9.txt").read().rstrip().split(',')

	for part in [1, 2]:
		a = Intcode(_input).run(_input=[part])
		print(f'PART {part}: {a._output}')  # 2789104029, 32869
