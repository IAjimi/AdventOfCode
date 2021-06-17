from collections import defaultdict

class Intcode():
	def __init__(self, program, noun=None, verb=None):
		self.program = defaultdict(int)
		for ix, val in enumerate(program):
			self.program[ix] = int(val)

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
			raise Exception(f'Invalid mode: {mode}, param: {param}.')

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

	def decode_output(self):
		decoded_output = ''.join([chr(c) for c in self._output]).splitlines()
		for line in decoded_output:
			print(line)

	def run(self, _input=[]):
		while self.i <= len(self.program):
			self.done = False
			instruction = self.program[self.i]
			opcode = instruction % 100
			param_mode = str(instruction // 100)
			param_mode = param_mode[::-1] + '0' * (3 - len(param_mode))
			ix_change = False
			#print(self.i, instruction)

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
					#self.decode_output()
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
				self.decode_output()
				return self
			else:
				raise Exception(f'Unknown opcode: {opcode}, instruction: {instruction}, param_mode: {param_mode}, index: {self.i}.')

			if not ix_change:
				self.i += 1 + len(params)


if __name__ == '__main__':
	_input = open("2019/aoc23.txt").read().rstrip().split(',')  # 17949, 12326

	network = {r: [Intcode(_input), [r]] for r in range(50)}
	searching = True
	delivered = []

	while searching:
		idle = 0

		for address, v in network.items():
			computer, packets = v

			if not packets:
				packets = [-1]
				idle += 1

			computer = computer.run(packets)

			while computer._output:
				dest = computer._output.pop(0)
				x = computer._output.pop(0)
				y = computer._output.pop(0)

				if dest == 255:
					if not delivered:
						print(f'PART 1: {y}')
					nat = [x, y]
				else:
					network[dest][1].extend([x, y])

			network[address] = [computer, packets]

		if idle == 50:
			network[0][1] = nat
			if nat[1] in delivered:
				print(f'PART 2: {nat[1]}')
				break
			delivered.append(nat[1])

