from itertools import permutations

class Intcode():
	def __init__(self, program, noun=None, verb=None):
		self.program = [int(i) for i in program]

		if noun:
			self.program[1] = noun
		if verb:
			self.program[2] = verb

		self.i = 0
		self._output = None

	def parameter_mode(self, mode, param):
		if mode == '0':
			return self.program[param]
		elif mode == '1':
			return param
		else:
			raise Exception('Invalid mode.')

	def get_params(self, param_mode, n_params):
		params = [None for n in range(n_params)]
		params[0] = self.parameter_mode(param_mode[0], self.program[self.i + 1])
		params[1] = self.parameter_mode(param_mode[1], self.program[self.i + 2])
		if n_params == 3:
			params[2] = self.program[self.i + 3]
		return params

	def run(self, _input):
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
				params = [self.program[self.i + 1]]
				current_input = _input[0]
				_input.pop(0)
				self.program[params[0]] = current_input
			elif opcode == 4:
				params = [self.parameter_mode(param_mode[0], self.program[self.i + 1])]
				self._output = params[0]
				self.i += 1 + len(params) # still need to increment!
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
			elif opcode == 99:
				self._output = self.program[0]
				return self
			else:
				raise Exception('Unknown opcode.')

			if not ix_change:
				self.i += 1 + len(params)

def amplifier_controller(_input):
	signals = []
	perm = list(permutations([0, 1, 2, 3, 4]))
	for thruster in perm:
		a = Intcode(_input).run([thruster[0], 0])
		b = Intcode(_input).run([thruster[1], a._output])
		c = Intcode(_input).run([thruster[2], b._output])
		d = Intcode(_input).run([thruster[3], c._output])
		e = Intcode(_input).run([thruster[4], d._output])
		signals.append(e._output)

	return signals, perm

def feedback_loop(_input):
	signals = []
	perm = list(permutations([5, 6, 7, 8, 9]))
	for thruster in perm:
		a = Intcode(_input).run([thruster[0], 0])
		b = Intcode(_input).run([thruster[1], a._output])
		c = Intcode(_input).run([thruster[2], b._output])
		d = Intcode(_input).run([thruster[3], c._output])
		e = Intcode(_input).run([thruster[4], d._output])

		while a.program[a.i] != 99:
			a = a.run([e._output])
			b = b.run([a._output])
			c = c.run([b._output])
			d = d.run([c._output])
			e = e.run([d._output])
			e_val = e._output

		signals.append(e_val)

	return signals, perm

def run(_input, part):
	if part == 1:
		signals, perm = amplifier_controller(_input)
	elif part == 2:
		signals, perm = feedback_loop(_input)
	else:
		raise Exception('Only 2 parts to this problem.')

	best_signal = max(signals)  # 4215746
	optimal_thruster = perm[signals.index(best_signal)]
	print(f'PART {part}: highest signal: {best_signal}, best thruster combination: {"".join([str(s) for s in optimal_thruster])}')



if __name__ == '__main__':
	_input = open("2019/aoc7.txt").read().split(',')
	run(_input, part=1)  # 844468
	run(_input, part=2)  # 4215746
