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
					#import pdb; pdb.set_trace()
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

def get_grid(_input, print_grid=False):
	grid = {}
	for x in range(50):
		line = []
		for y in range(50):
			val = Intcode(_input).run([x,y])._output[0]
			grid[(x, y)] = val
			if val == 0:
				line.append('.')
			else:
				line.append('#')

		if print_grid: print(' '.join(line))
	return grid

def get_slopes(_input):
	x = 0
	y = 10000

	while Intcode(_input).run([x,y])._output[0] == 0:
		x += 1
	x1 = x
	while Intcode(_input).run([x,y])._output[0] == 1:
		x += 1
	x2 = x
	return y / x2, y / x1


def search_beams(m1, m2):
	'''
	Borrows from https://topaz.github.io/paste/#XQAAAQDeBwAAAAAAAAAzHIoib6pMX4gszwa4sWe2v/YEWnXtlGxbTY+nmmg/bWuDvrVEtKJlqGgAA9bZn/7XEJM5D/hi0qmvZeru1MlMZoVDNQPB9QGE1I3hV9V3zXMyJ+hYvACr8Kbm2GygmS+Br3b0TIlHItfaMnU5wXxw7PHu5r6/MrUioaZcuiBFy6hdkfhmqxEp7A26tMJAL8pYBnb3QjsiKjKqH/y0+2Rjz07+K5fMhUUbq6Zn4G77UrPQPYX5yhPdqdvnP40P4NsN2qFFdasTlDySrzi4cPklhdvo99k7nZm1RpoO2YWm2HfJ+xD6MOx8Yp2AKauegT48ZWuUzuFbXM0sMXhC3jjX5Fc3wAkHV20BmkAlKqDvyYWlys+UzAs4AlYElhd4Lj4jrqSJH+V9NWNBxntUm/mtDJzDYaOSSftZQ13Re1xZwY4EBf6xQeuWHD4jk27bnl3FObkEMPBm3ztFI8BDhPRncjAkXfumQT6bQ/W/jjVJd6bOrAfTV1q1ghdH6v5oa89J1nHna2ZKsCOJzgYMT7WjSwtPdiU2nzTE4QG9+ZeNAmHRdIvrNtPF6NLurH68zvFInIPvD8CH6fywl+XqcnAknDOmM4M1WCaOSLDxCtX/QfY5jJM1E4vZwdo2yoHql1lL9+8jc+O2sxhjz/2NJ2ujUIeAFm/X+tuwzXh6ntSa1v6Iptp6zbfLHu7Hp4V4T03KzCgCWXBpCXeGGqUk/l38g0bWbqcvTQUiUGz83T7Db4dBAP0Olu8WSU01NJz9bCQ3ZWW8Rtpo4EuIX1LN16MK2PUpbodgqzB9y2rUfz9REHgHDCjxyEV/R4d96U6K6M9MbFb0sb2FFCz+MgS5yPwEAZLG7J4DB5AQZA1M2/NT20GRJccyUZKH1wtoQoUG1vepU3fCvT9PhuJmBgEfmXHdCu8F0F6bSB/5RasYi722u4HkkH7Du4DOkwk9cKDuztpTOK2j1FJp2IavMMgIZ3wALOe6FpJM3b3Twb5ekKIXegaGkC3uIFV8va2V7iADtqlYJWY+GQbjOpi4zdO0n7mR5QQNuoxIAK8pSguzzhbMy3o630iThQg4oqIbGj9u8ZPuHcv1SYe0rP0kXGoi+k32aSSC/++kS7c=
	to get the slopes of the lines of the tractor beams + an initial guess (which is wrong).

	This then uses the slope of the bottom left corner, m1, to find the coordinates of the top left corner
	of the first 100x100 square that can fit within the tractor beams.

	:param m1: float, slope of bottom left corner
	:param m2: float, slope of bottom right corner
	:return: int, solution using coordinates of top left corner
	'''
	x2 = ((m1 * 99) + 99) / (m2 - m1)
	y1 = round((m2 * x2) - 99)
	found = False

	while not found:
		x1 = round(y1 / m2)
		x2, y2 = x1 + 99, y1 - 99

		r1 = Intcode(_input).run([x1, y1])._output[0]  # bottom left corner
		r2 = Intcode(_input).run([x2, y2])._output[0]  # top right corner

		if r1 == 1 and r2 == 1:
			return x1 * 10000 + y1 - 99
		else:
			y1 += 1

	return 0

if __name__ == '__main__':
	_input = open("2019/aoc19.txt").read().rstrip().split(',')

	grid = get_grid(_input, print_grid=False)
	tractor_beam = sum([1 for v in grid.values() if v == 1])  # 203
	print(f'PART 1: {tractor_beam}')

	m1, m2 = get_slopes(_input)
	sol2 = search_beams(m1, m2)  # 8771057
	print(f'PART 2: {sol2}')



