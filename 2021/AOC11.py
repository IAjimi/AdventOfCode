"""
1st day making it in the top 1000 with ranks 825 and 702 for part 1 and 2 respectively.
Was able to reuse some code from day 9 for the grid + get_neighbors function.
Using a queue to keep track of 'flashing' octopi.
"""

from _utils import read_input, timer


def get_neighbors(grid: dict, pos: tuple):
    x, y = pos
    neighbors = [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
    neighbors = [n for n in neighbors if n in grid and n != pos]
    return neighbors


def run_step(grid):
    grid = {pos: val + 1 for pos, val in grid.items()}
    flash_queue = [pos for pos, val in grid.items() if val > 9]
    has_flashed = set()

    while flash_queue:
        current_octopus = flash_queue.pop()

        if current_octopus not in has_flashed:
            has_flashed.add(current_octopus)
            neighbors = get_neighbors(grid, current_octopus)

            # Update grid, add to flash set if needed
            for n in neighbors:
                grid[n] += 1
                if grid[n] > 9:
                    flash_queue.append(n)

    # Reset vals of octopi that flashed
    for octopus in has_flashed:
        grid[octopus] = 0

    return grid, len(has_flashed)


def simulate_octopi(grid):
    """
    Returns tuple of part_1_score, part_2_score.

    The convergence of all octopi flashing happens
    *after* 100 steps (at least in my input), hence the while counter.
    """
    part_1_score, step, counter = 0, 0, 0

    while counter != 100:
        grid, counter = run_step(grid)
        if step < 100:
            part_1_score += counter
        step += 1

    return part_1_score, step


@timer
def main(filepath: str):
    _input = read_input(filepath)
    _input = [[int(char) for char in line] for line in _input]
    grid = {
        (x, y): _input[y][x] for y in range(len(_input)) for x in range(len(_input[0]))
    }

    part_1_score, part_2_score = simulate_octopi(grid)

    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc11.txt")
    print(f"PART 1: {part_1_score}")  # 1659
    print(f"PART 2: {part_2_score}")  # 227
