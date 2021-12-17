from _utils import read_input, timer
import parse


class ProbeLauncher:
    def __init__(self, filepath: str, max_steps: int = 180):
        _input = read_input(filepath)
        string = _input[0]
        self.min_x, self.max_x, self.min_y, self.max_y = tuple(
            parse.parse("target area: x={:d}..{:d}, y={:d}..{:d}", string).fixed
        )
        self.max_steps = max_steps

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
        max_y_reached = y

        for step in range(self.max_steps):
            # Update position and velocity of projectile
            x, y, x_velocity, y_velocity = self.adjust_projectile(
                x, y, x_velocity, y_velocity
            )

            # Get max_y_reached
            max_y_reached = max(max_y_reached, y)

            # In target range
            if (self.min_x <= x <= self.max_x) and (self.min_y <= y <= self.max_y):
                return True, max_y_reached
            # Target has overshot x range (moving too far right)
            elif x_velocity > 0 and x > self.max_x:
                return False, 0
            # Target has failed to reach x range (moving left without reaching x range)
            elif x_velocity < 0 and x < self.max_x:
                return False, 0
            # Outside of x target range & stopped moving
            elif x_velocity == 0 and (x < self.min_x or x > self.max_x):
                return False, 0
            # Is permanently below min y range
            elif y_velocity < 0 and y < self.min_y:
                return False, 0

        return False, 0

    def main(self):
        """
        Finds the highest y that can be reached by a probe and
        the number of probes that can reach the target area.

        The list of test probe velocities (test_probes) is done as follows:
            * for an input where the target x range is >= 0, the minimum x
            velocity vx is += 0 (otherwise won't move in correct direction)
            * the max x velocity of a probe must be the end of the target range,
            since any higher velocity will overshoot it and miss the mark
            * similarly, the min y velocity (with a < 0 y range) must be the
            beginning of the y target range
        """
        test_probes = [
            (vx, vy)
            for vx in range(0, self.max_x + 1)  # for inputs where target x range >= 0
            for vy in range(self.min_y, 100)  # for inputs where target y <= 0
        ]
        max_y_reached = 0
        reach_target_probes = set()

        for probe in test_probes:
            reaches_target, new_max_y = self.launch_projectile(probe[0], probe[1])
            if reaches_target:
                reach_target_probes.add(probe)
                max_y_reached = max(max_y_reached, new_max_y)

        return max_y_reached, len(reach_target_probes)


@timer
def main(filepath: str):
    """
    Returns part 1 & 2 scores from a filepath.
    """
    part_1_score, part_2_score = ProbeLauncher(filepath, max_steps=180).main()
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc17.txt")
    print(f"PART 1: {part_1_score}")  # 3003
    print(f"PART 2: {part_2_score}")  # 940
