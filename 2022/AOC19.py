import functools
import parse

from _utils import read_input, timer, Solution


def process_input(filename: str):
    _input = read_input(filename)
    blueprints = []
    for line in _input:
        _id, o_o, c_o, obs_o, obs_c, geo_o, geo_obs = tuple(parse.parse("Blueprint {:d}: Each ore robot costs {:d} ore. Each clay robot costs {:d} ore. Each obsidian robot costs {:d} ore and {:d} clay. Each geode robot costs {:d} ore and {:d} obsidian.", line).fixed)
        blueprints.append(((o_o,0,0),(c_o,0,0),(obs_o,obs_c,0),(geo_o,0,geo_obs)))
    return blueprints

@functools.lru_cache(maxsize=None)
def collect_geodes(
    t, ore_robot, clay_robot, obs_robot, geode_robot, ore, clay, obisidian, geode, blueprint
):
    if t <= 0:
        return geode

    options = []
    max_ore_spend = max(o for o,*_ in blueprint)
    max_clay_spend = max(c for _,c,*_ in blueprint)
    max_obs_spend = max(obs for _,_,obs in blueprint)

    new_ore = min(ore + ore_robot, max_ore_spend * t)  # most ore you could spend in rest of run
    new_clay = min(clay + clay_robot, max_clay_spend * t)
    new_obs = min(obisidian + obs_robot, max_obs_spend * t)
    new_geode = geode + geode_robot

    # always build geode robot
    if (
        blueprint[3][0] <= ore
        and blueprint[3][2] <= obisidian
    ):
        options.append(
            collect_geodes(
                t - 1,
                ore_robot,
                clay_robot,
                obs_robot,
                geode_robot + 1,
                new_ore - blueprint[3][0],
                new_clay,
                new_obs - blueprint[3][2],
                new_geode,
                blueprint
            )
        )
    else:
        # build nothing
        options.append(
            collect_geodes(
                t - 1,
                ore_robot,
                clay_robot,
                obs_robot,
                geode_robot,
                new_ore,
                new_clay,
                new_obs,
                new_geode,
                blueprint
            )
        )

        # build new ore robot
        if blueprint[0][0] <= ore and ore_robot < max_ore_spend:
            options.append(
                collect_geodes(
                    t - 1,
                    ore_robot + 1,
                    clay_robot,
                    obs_robot,
                    geode_robot,
                    new_ore - blueprint[0][0],
                    new_clay,
                    new_obs,
                    new_geode,
                    blueprint
                )
            )

        # build new clay robot
        if blueprint[1][0] <= ore and clay_robot < max_clay_spend:
            options.append(
                collect_geodes(
                    t - 1,
                    ore_robot,
                    clay_robot + 1,
                    obs_robot,
                    geode_robot,
                    new_ore - blueprint[1][0],
                    new_clay,
                    new_obs,
                    new_geode,
                    blueprint
                )
            )

        # build new obsidian robot
        if (
            blueprint[2][0] <= ore
            and blueprint[2][1] <= clay
            and obs_robot < max_obs_spend
        ):
            options.append(
                collect_geodes(
                    t - 1,
                    ore_robot,
                    clay_robot,
                    obs_robot + 1,
                    geode_robot,
                    new_ore - blueprint[2][0],
                    new_clay - blueprint[2][1],
                    new_obs,
                    new_geode,
                    blueprint
                )
            )

    return max(options)


def part1(blueprints):
    quality_levels = []
    for i, bp in enumerate(blueprints, start=1):
        geodes = collect_geodes(24, 1, 0, 0, 0, 0, 0, 0, 0, bp)
        print(f"max geodes collected with blueprint {i} are {geodes}")
        quality_levels.append((i)*geodes)
    return sum(quality_levels)


def part2(blueprints):
    solution = 1
    for i, bp in enumerate(blueprints[:3], start=1):
        geodes = collect_geodes(32, 1, 0, 0, 0, 0, 0, 0, 0, bp)
        print(f"max geodes collected with blueprint {i} are {geodes}")
        solution *= geodes
    return solution

@timer
def main(filename: str) -> Solution:
    blueprints = process_input(filename)
    part_1_solution = part1(blueprints)
    part_2_solution = part2(blueprints)
    return part_1_solution, part_2_solution


if __name__ == "__main__":
    part_1_solution, part_2_solution = main("aoc19.txt")
    print(f"PART 1: {part_1_solution}")  # 1092
    print(f"PART 2: {part_2_solution}")  # 3542
