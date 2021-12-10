from _utils import read_input, timer


def spell_checker(line: str):
    """
    Returns a tuple of points: pt1_score, pt2_score.
    """
    stack = []
    matching_char = {"(": ")", "{": "}", "[": "]", "<": ">"}
    corrupt_points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    incomplete_points = {"(": 1, "[": 2, "{": 3, "<": 4}

    # Create stack, return part 1 score if corrupt
    for char in line:
        if char in matching_char:
            stack.append(char)
        else:
            opening_char = stack.pop()
            if matching_char[opening_char] != char:
                return corrupt_points[char], 0

    # Use stack to compute part 2 score
    score = 0
    for char in reversed(stack):
        score *= 5
        score += incomplete_points[char]

    return 0, score


@timer
def main(filepath: str):
    _input = read_input(filepath)

    scores = [spell_checker(line) for line in _input]

    part_1_score = sum([pt1_score for pt1_score, pt2_score in scores])

    part_2_score = [pt2_score for pt1_score, pt2_score in scores if pt2_score > 0]
    part_2_score.sort()
    part_2_score = part_2_score[len(part_2_score) // 2]

    return part_1_score, part_2_score


if __name__ == "__main__":
    # 7:10 - 7:27 total
    part_1_score, part_2_score = main("aoc10.txt")
    print(f"PART 1: {part_1_score}")  # 367227
    print(f"PART 2: {part_2_score}")  # 3583341858