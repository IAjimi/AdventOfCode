from _utils import read_input, timer

def parse_input(_input:list):
    image_enhancement_algo = _input[0]
    _input = _input[2:]
    grid = {
        (x, y): _input[x][y] for x in range(len(_input)) for y in range(len(_input[0]))
    }
    return image_enhancement_algo, grid

def get_neighbors(pos: tuple):
    """
    Returns the 9 positions centered around pos (x,y).
    Neighbors list should be ordered from top left to bottom right.
    """
    neighbors = [(pos[0] + dx, pos[1] + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
    return neighbors


def expand_grid(grid: dict, step: int):
    """
    Expands grid dict to take into account relevant pixels.

    In theory the grid is infinite but the pixels that do not
    have an "active" pixel next to them (all "."s) just flip
    between "." and "#" every step.
    """
    new_grid = grid.copy()
    for pos in grid.keys():
        neighbors = get_neighbors(pos)
        for n in neighbors:
            if n not in new_grid:
                new_grid[n] = "." if step % 2 == 0 else "#"

    return new_grid


def enhance_picture(grid: dict, image_enhancement_algo: str, step: int):
    new_grid = {}

    for pos, pixel in grid.items():
        # get neighbors
        neighbors = get_neighbors(pos)

        bin_string = ""
        for n in neighbors:
            # either are tracked
            if n in grid:
                bin_string += grid[n]
            # or not (in which case take default value)
            else:
                bin_string += "." if step % 2 == 0 else "#"

        bin_string = "".join(["1" if c == "#" else "0" for c in bin_string])
        bin_num = int(bin_string, 2)
        new_pixel = image_enhancement_algo[bin_num]
        new_grid[pos] = new_pixel

    return new_grid

def count_lit_pixels(grid: dict):
    return sum([1 for v in grid.values() if v == "#"])

@timer
def main(filepath: str):
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = read_input(filepath)
    image_enhancement_algo, grid = parse_input(_input)

    for step in range(50):
        grid = expand_grid(grid, step)
        grid = enhance_picture(grid, image_enhancement_algo, step)
        if step == 1:
            part_1_score = count_lit_pixels(grid)

    part_2_score = count_lit_pixels(grid)
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc20.txt")
    print(f"PART 1: {part_1_score}")  # 5291
    print(f"PART 2: {part_2_score}")  # 16665
