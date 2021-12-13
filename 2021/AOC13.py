from _utils import read_input, timer

def parse_input(_input: list):
    grid = set()
    instructions = []

    for line in _input:
        if ',' in line:
            x, y = line.split(',')
            x, y = int(x), int(y)
            grid.add((x,y))
        elif 'fold along' in line:
            instructions.append(line)

    return grid, instructions

def vertical_flip(grid: set, flip_val:int):
    new_grid = set()
    for x,y in grid:
        if y > flip_val:
            new_y = 2 * flip_val - y
            new_grid.add((x, new_y))
        else:
            new_grid.add((x, y))
    return new_grid


def horizontal_flip(grid: set, flip_val:int):
    new_grid = set()
    for x,y in grid:
        if x > flip_val:
            new_x = 2 * flip_val - x
            new_grid.add((new_x, y))
        else:
            new_grid.add((x, y))
    return new_grid

def print_grid(grid:set):
    grid_str = ''
    max_x = 1 + max((pos[0] for pos in grid))
    max_y = 1 + max((pos[1] for pos in grid))

    for y in range(max_y):
        line = []
        for x in range(max_x):
            if (x,y) in grid:
                line.append('#')
            else:
                line.append('.')
        grid_str += ' '.join(line)
        grid_str += '\n'

    return grid_str

@timer
def main(filepath: str):
    _input = read_input(filepath)
    grid, instructions = parse_input(_input)

    for ix, instr in enumerate(instructions):
        _, flip_val = instr.split('=')
        flip_val = int(flip_val)

        if 'x' in instr:
            grid = horizontal_flip(grid, flip_val)
        elif 'y' in instr:
            grid = vertical_flip(grid, flip_val)

        if ix == 0:
            part_1_score = len(grid)

    return part_1_score, grid


if __name__ == "__main__":
    part_1_score, part_2_grid = main("aoc13.txt")
    print(f"PART 1: {part_1_score}")  # 850
    print(f"PART 2: \n {print_grid(part_2_grid)}")  # AHGCPGAU
