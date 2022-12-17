import heapq
import itertools
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

    return enhanced_network, valves


def part1(valves, network):
    network, valves = build_network(valves, network)

    def find_path(t: int, valve: str, state: Tuple[str, int], seen) -> int:
        current_pressure = sum(
            (opened_time - t) * valves[v] for v, opened_time in state
        )
        if seen.get((t, valve), -1) >= current_pressure:
            return 0
        seen[t, valve] = current_pressure

        if t <= 0 or len(state) == len(valves):
            return current_pressure

        # choice 1: wait
        wait = find_path(t - 1, valve, state, seen)

        # choice 2: move to unopened valve and open it
        # (!important: only USEFUL valves + eliminate state where move solely!)
        # (requires precomputing distances from current valve to neighbors w/ >0 pressure flow)
        max_new_valve = 0
        neighbors = network[valve]
        for new_valve, dist, p in neighbors:
            opened_valves = [v for v, _ in state]
            if new_valve not in opened_valves and t - dist > 0:
                new_state = [
                    (v, tt) for v, tt in state
                ]  # convert tuple to list to add new element
                new_state.append((new_valve, t - dist))
                new_pressure = find_path(
                    t - dist, new_valve, tuple(new_state), seen
                )  # convert back
                max_new_valve = max(max_new_valve, new_pressure)

        return max(wait, max_new_valve)

    return find_path(30, "AA", (), {})


def part2(valves, network, max_t=26):
    def find_path(t: int, valve_a: str, valve_b: str, state, seen) -> int:
        current_pressure = sum(
            (opened_time - t) * valves[v] for v, opened_time in state
        )
        if seen.get((t, valve_a, valve_b), -1) >= current_pressure:
            return 0
        seen[t, valve_a, valve_b] = current_pressure

        if t <= 0 or len(state) == len(valves):
            return current_pressure

        options = [0]
        opened_valves = [v for v, _ in state]

        # consider all options
        for new_valve_a in network[valve_a] + [valve_a]:
            # player A opens current valve
            if (
                valve_a == new_valve_a
                and valve_a not in opened_valves
                and valves[valve_a] > 0
            ):
                for new_valve_b in network[valve_b] + [valve_b]:
                    # update state
                    new_state = [(v, tt) for v, tt in state]
                    new_state.append((new_valve_a, t))

                    # A - player E moves to new valve
                    future_value = find_path(
                        t - 1, new_valve_a, new_valve_b, new_state, seen
                    )
                    options.append(future_value)

                    # B - player E opens current valve
                    if (
                        valve_b == new_valve_b
                        and new_valve_b != new_valve_a
                        and new_valve_b not in opened_valves
                        and valves[new_valve_b] > 0
                    ):
                        new_state.append((new_valve_b, t))
                        future_value = find_path(
                            t - 1, new_valve_a, new_valve_b, new_state, seen
                        )
                        options.append(future_value)
                        new_state.pop()
            # player A moves to new valve
            else:
                for new_valve_b in network[valve_b] + [valve_b]:
                    # A - player E moves to new valve
                    future_value = find_path(
                        t - 1, new_valve_a, new_valve_b, state, seen
                    )
                    options.append(future_value)

                    # B - player E opens current valve
                    if (
                        valve_b == new_valve_b
                        and new_valve_b != new_valve_a
                        and new_valve_b not in opened_valves
                        and valves[new_valve_b] > 0
                    ):
                        # update state
                        new_state = [(v, tt) for v, tt in state]
                        new_state.append((new_valve_b, t))
                        future_value = find_path(
                            t - 1, new_valve_a, new_valve_b, new_state, seen
                        )
                        options.append(future_value)
                        new_state.pop()

        return max(options)

    return find_path(max_t - 1, "AA", "AA", (), {})


@timer
def main(filename: str) -> Solution:
    valves, network = process_input(filename)
    part_1_solution = part1(valves, network)
    part_2_solution = part2(valves, network)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc16.txt")
    print(f"PART 1: {part_1_solution}")  # 1789
    print(f"PART 2: {part_2_solution}")  # 2496
