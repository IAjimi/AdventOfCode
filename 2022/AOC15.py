from typing import List, Dict
import parse
from _utils import read_input, timer, Solution, Point


MAX_Y = 4_000_000


def process_input(filename: str) -> Dict[Point, int]:
    _input = read_input(filename)

    sensors = {}
    for line in _input:
        x1, y1, x2, y2 = tuple(
            parse.parse(
                "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}", line
            ).fixed
        )

        sensors[(x1, y1)] = manhattan_distance((x1, y1), (x2, y2))
    return sensors


def manhattan_distance(t1: Point, t2: Point) -> int:
    x1, y1 = t1
    x2, y2 = t2
    return abs(x1 - x2) + abs(y1 - y2)


class Intervals:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals = sorted(intervals, key=lambda i: i[0])
        l, r = 0, 1

        while r <= len(intervals) - 1:
            if intervals[l][0] <= intervals[r][0] <= intervals[l][1]:
                intervals[l][0] = min(intervals[l][0], intervals[r][0])
                intervals[l][1] = max(intervals[l][1], intervals[r][1])
                del intervals[r]
            else:
                l += 1
                r += 1

        return intervals


def check_line(sensors: Dict[Point, int], Y: int, part1: bool) -> List[List[int]]:
    intervals = []

    for pos, distance in sensors.items():
        x1, y1 = pos
        distance_to_y = abs(y1 - Y)
        remaining_distance = distance - distance_to_y

        if remaining_distance >= 0:
            if part1:
                intervals.append([x1 - remaining_distance, x1 + remaining_distance])
            else:
                min_x = max(0, x1 - remaining_distance)
                max_x = min(MAX_Y, x1 + remaining_distance)
                if min_x <= MAX_Y:
                    intervals.append([min_x, max_x])

    return Intervals().merge(intervals)


def part1(sensors: Dict[Point, int]):
    intervals = check_line(sensors, 2_000_000, part1=True)
    interval_length = intervals[0][1] - intervals[0][0]
    return interval_length


def part2(sensors: Dict[Point, int]):
    for y in range(MAX_Y, 0, -1):
        intervals = check_line(sensors, y, part1=False)
        if len(intervals) != 1:
            x = intervals[0][1] + 1
            return x * 4_000_000 + y
    return 0


@timer
def main(filename: str) -> Solution:
    sensors = process_input(filename)
    part_1_solution = part1(sensors)
    part_2_solution = part2(sensors)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc15.txt")
    print(f"PART 1: {part_1_solution}")  # 4907780
    print(f"PART 2: {part_2_solution}")  # 13639962836448 (3409990, 2836448)
