from _utils import read_input, timer
import parse

class Probe:
    def __init__(self, _input:list, max_steps:int):
        self.max_steps = max_steps
        string = _input[0]
        self.min_x, self.max_x, self.min_y, self.max_y = tuple(parse.parse('target area: x={:d}..{:d}, y={:d}..{:d}', string).fixed)

    def adjust_projectile(self, x: int, y: int, x_velocity: int, y_velocity: int):
        x += x_velocity
        y += y_velocity

        if x_velocity > 0:
            x_velocity += -1
        elif x_velocity < 0:
            x_velocity += 1

        y_velocity += -1

        return x, y, x_velocity, y_velocity


    def launch_projectile(self, x_velocity: int, y_velocity: int):
        x, y = 0, 0
        max_y = -10**10

        for step in range(self.max_steps):
            x, y, x_velocity, y_velocity = self.adjust_projectile(x, y, x_velocity, y_velocity)

            # Get max_y
            max_y = max(max_y, y)

            # In target range
            if (self.min_x <= x <= self.max_x) and (self.min_y <= y <= self.max_y):
                return True, max_y
            # Outside of x target range & stopped moving
            elif (x_velocity == 0 and (x < self.min_x or x > self.max_x)):
                return False, 0
            # Has fallen outside y range
            elif (y_velocity < 0 and y < self.min_y):
                return False, 0

        return False, 0

    def main(self):
        max_range = 290
        test_probes = [(vx,vy) for vx in range(-max_range, max_range) for vy in range(-max_range,max_range)]
        max_y = -10**10
        reach_target_probes = set()


        for probe in test_probes:
            reaches_target, step, new_max_y = self.launch_projectile(probe[0], probe[1])
            if reaches_target:
                reach_target_probes.add(probe)
                max_y = max(max_y, new_max_y)
            #print(probe, reaches_target, step, max_y)

        return max_y, len(reach_target_probes)



@timer
def main(filepath: str):
    """
    Returns part 1 & 2 scores from a filepath.
    """
    _input = read_input(filepath)
    part_1_score, part_2_score = Probe(_input, max_steps=180).main()
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc17.txt")
    print(f"PART 1: {part_1_score}")  # 3003
    print(f"PART 2: {part_2_score}")  # 940
