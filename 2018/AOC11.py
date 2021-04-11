def find_power_level(point, grid_serial_number):
    """Computes the power level of a point given a
    grid serial number."""
    x, y = point

    rack_id = x + 10
    power_level = (rack_id * y) + grid_serial_number
    power_level = power_level * rack_id
    power_level = (power_level % 1000) // 100  # keep only hundreds digit
    power_level = power_level - 5

    return power_level


def find_grid_power_level(point, size, power_level_points):
    """Finds the total power level for the 3x3 grid
    formed by having point in the top left corner."""
    x, y = point
    grid_points = [(x + xx, y + yy) for xx in range(size) for yy in range(size)]
    power_grid_points = [power_level_points[p] for p in grid_points if p in power_level_points.keys()]
    return sum(power_grid_points)


def main(grid_serial_number, size):
    # Generates points
    points = [(x, y) for x in range(1, 301) for y in range(1, 301)]

    # Calculates power level of the points
    power_level_points = {p: find_power_level(p, grid_serial_number) for p in points}

    # Finds sum of power level in grid
    power_grid_points = {p: find_grid_power_level(p, size, power_level_points) for p in points}

    # Find point with the highest power level in its grid
    square_values = list(power_grid_points.values())
    max_square_value_loc = square_values.index(max(square_values))
    max_square_value_point = list(power_grid_points.keys())[max_square_value_loc]

    return max_square_value_point, max(square_values)


if __name__ == "__main__":
    grid_serial_number = 6878
    sol1 = main(grid_serial_number, 3)  # 20, 34
    print(f'PART 1: {sol1}')

    sol2 = [main(grid_serial_number, g) for g in range(3, 20)]
    sol2_ix = [s[1] for s in sol2]
    sol2_ix = sol2_ix.index(max([s[1] for s in sol2]))

    print(f'PART 2: {sol2[sol2_ix]}')  # 90,57,15
