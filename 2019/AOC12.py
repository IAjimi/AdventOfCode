import time
import math
import numpy as np


def lcm(a, b):
	return a * b // math.gcd(a, b)

def parse_input(line):
	line = line[1:-1].split(', ')  # removes < >, then splits
	line = [int(s[2:]) for s in line]
	return line

def clean_input(_input):
	positions = [parse_input(line) for line in _input]

	x = np.array([coord[0] for coord in positions])
	y = np.array([coord[1] for coord in positions])
	z = np.array([coord[2] for coord in positions])

	velocity_x = np.array([0 for coord in positions])
	velocity_y = np.array([0 for coord in positions])
	velocity_z = np.array([0 for coord in positions])

	return x, y, z, velocity_x, velocity_y, velocity_z

def apply_gravity(pos, velocity):
	for ix in range(len(pos)):
		n = 0
		val = pos[ix]
		for v in pos:
			if val < v:
				n += 1
			elif val > v:
				n += -1

		velocity[ix] += n

	pos = pos + velocity

	return pos, velocity

def calculate_energy(points, points_velocity):
	energy = 0
	for ix in range(len(points)):
		pot = sum([abs(p) for p in points[ix]])
		kin = sum([abs(p) for p in points_velocity[ix]])
		energy += pot * kin

	return energy

def save_trajectory(turn, pos, og_k, past_list):
	k = ''.join([str(p) for p in pos])
	if k == og_k:
		past_list.append(turn)
	return past_list

def run(_input, turns, part=1):
	x, y, z, velocity_x, velocity_y, velocity_z = clean_input(_input)

	# Save initial states
	if part == 2:
		og_x = ''.join([str(p) for p in x])
		og_y = ''.join([str(p) for p in y])
		og_z = ''.join([str(p) for p in z])
		past_x, past_y, past_z = [], [], []

	# Simulate movement
	for r in range(turns):
		x, velocity_x = apply_gravity(x, velocity_x)
		y, velocity_y = apply_gravity(y, velocity_y)
		z, velocity_z = apply_gravity(z, velocity_z)

		if part == 2:
			past_x = save_trajectory(r, x, og_x, past_x)
			past_y = save_trajectory(r, y, og_y, past_y)
			past_z = save_trajectory(r, z, og_z, past_z)

	# Calculate energy
	if part == 1:
		points = list(zip(x, y, z))
		points_velocity = list(zip(velocity_x, velocity_y, velocity_z))
		energy = calculate_energy(points, points_velocity)

		return energy

	# Find Cycle
	elif part == 2:
		lcd_x = past_x[1] + 1  # +1 because first appearance isn't recorded in list
		lcd_y = past_y[1] + 1
		lcd_z = past_z[1] + 1

		print(lcd_x, lcd_y, lcd_z)  # 113028 167624 231614
		return lcm(lcm(lcd_x, lcd_y), lcd_z)

if __name__ == '__main__':
	_input = '''<x=-4, y=-9, z=-3>
<x=-13, y=-11, z=0>
<x=-17, y=-7, z=15>
<x=-16, y=4, z=2>'''.splitlines()
	energy = run(_input, 1000, part=1)  # 6220
	print(f'PART 1: {energy}')

	t0 = time.time()
	cycles = run(_input, 250000, part=2)  # 548525804273976
	t1 = time.time() - t0
	print(f'PART 2: {cycles}, speed: {round(t1, 2)}')  # += 12 sec