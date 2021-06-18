from collections import defaultdict
from itertools import combinations

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
				raise Exception('Unknown opcode.')

			if not ix_change:
				self.i += 1 + len(params)


def translate_to_ascii(instructions):
	instructions = [ord(c) for c in instructions]
	instructions.append(10)

	return instructions

def brute_force_inventory(computer, inventory):
	'''Taken from https://github.com/LubosKolouch/adventofcode_2019/blob/master/25/t25.py

	Tries all possible combination of inventory items. Stops when the program hits 99 and
	prints out all of the text so far (which includes the password).'''
	for i in range(len(inventory) + 1):
		for comb in combinations(inventory, i):
			instr_str = []
			for inv in inventory:
				instr_str.extend(translate_to_ascii("drop " + inv))
			for item in comb:
				instr_str.extend(translate_to_ascii("take " + item))

			instr_str.extend(translate_to_ascii("south"))
			computer = computer.run(instr_str)
			if computer.program[computer.i] % 100 == 99:
				break

def run(_input):
	'''Exploration done manually. Prints out the password + text adventure for successful
	inventory combination.'''
	instructions = ['south', 'take food ration', 'west', 'take sand', 'north', 'north', 'east',
					'take astrolabe', 'west', 'south', 'south', 'east', 'north', 'north',
					'east', 'take coin', 'east', 'west', 'west', 'south', 'east', 'take cake',
					'south', 'take weather machine', 'west', 'take ornament', 'west', 'take jam',
					'east', 'east', 'north', 'east', 'east', 'east', 'south', 'inv'
					]

	computer = Intcode(_input).run()
	for instruc in instructions:
		computer = computer.run(translate_to_ascii(instruc))

	inventory = ['sand', 'coin', 'jam', 'astrolabe', 'ornament', 'weather machine', 'food ration', 'cake']
	brute_force_inventory(computer, inventory)

if __name__ == '__main__':
	_input = open("2019/aoc25.txt").read().rstrip().split(',')
	run(_input)  # ('astrolabe', 'ornament', 'weather machine', 'food ration') - 4206594
