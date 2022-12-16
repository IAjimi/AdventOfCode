import functools
import heapq
import itertools
from collections import defaultdict

import parse
from typing import List, Tuple, Set

from _utils import read_input, timer, Solution


def process_input(filename: str):
    _input = read_input(filename)

    valves = {}
    network = {}
    for line in _input:
        line = line.replace("valves", "valve").replace("tunnel leads", "tunnels lead")
        parsed_line = parse.parse(
            "Valve {start} has flow rate={flow_rate}; tunnels lead to valve {end}", line
        )
        start, flow_rate, end = (
            parsed_line["start"],
            int(parsed_line["flow_rate"]),
            parsed_line["end"].replace(" ", ""),
        )
        valves[start] = flow_rate
        network[start] = end.split(",")
    return valves, network


def find_shortest_path(network, start: str, end: str) -> int:
    queue = []
    heapq.heappush(queue, (0, start))
    visited = set()

    while queue:
        steps, current_node = heapq.heappop(queue)

        if current_node == end:
            return steps
        elif current_node not in visited:
            visited.add(current_node)

            neighbors = network[current_node]
            for next_node in neighbors:
                if next_node not in visited:
                    heapq.heappush(queue, (steps + 1, next_node))

    return -1


def build_network(valves, network):
    nodes = {n for n in network}
    enhanced_network = {}

    for (start, end) in itertools.product(nodes, nodes):
        dist = find_shortest_path(network, start, end)
        pressure = valves[end]
        if dist > 0 and pressure > 0:
            if start not in enhanced_network:
                enhanced_network[start] = [(end, 1 + dist, pressure)]
            else:
                enhanced_network[start].append(
                    (end, 1 + dist, pressure)
                )  # +1 for opening valve

    return enhanced_network


def part1(valves, network):
    network = build_network(valves, network)

    def find_path(t: int, valve: str, state) -> int:
        # TODO USE CACHE
        current_pressure = sum(
            (opened_time - t) * pressure for pressure, opened_time in state.values()
        )
        if t <= 0:
            return current_pressure

        # choice 1: wait
        wait = find_path(t - 1, valve, state)

        # choice 2: move to unopened valve and open it
        # (!important: only USEFUL valves + eliminate state where move solely!)
        # (requires precomputing distances from current valve to neighbors w/ >0 pressure flow)
        max_new_valve = 0
        neighbors = network[valve]
        for new_valve, dist, p in neighbors:
            if new_valve not in state and t - dist > 0:
                new_state = state.copy()
                new_state[new_valve] = p, t - dist  # valve pressure, time opened
                new_pressure = find_path(t - dist, new_valve, new_state)
                max_new_valve = max(max_new_valve, new_pressure)

        return max(wait, max_new_valve)

    return find_path(30, "AA", {})


@timer
def main(filename: str) -> Solution:
    valves, network = process_input(filename)
    part_1_solution = part1(valves, network)
    part_2_solution = 0
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc16.txt")  # 6:54
    print(f"PART 1: {part_1_solution}")  #
    print(f"PART 2: {part_2_solution}")  #
