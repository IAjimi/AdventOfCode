from _utils import read_input, timer


class Game:
    def __init__(self, filepath: str):
        _input = read_input(filepath)

        self.die = 1
        self.die_rolls = 0
        self.player1_space = int(_input[0].split(": ")[1])
        self.player2_space = int(_input[1].split(": ")[1])
        self.player1_score = 0
        self.player2_score = 0
        self.WINNING_SCORE = 1000

    def roll_die(self):
        self.die_rolls += 1
        self.die = (self.die + 1) % 100
        return self.die - 1

    def move_player(self, initial_space: int):
        dice_rolls = sum([self.roll_die() for _ in range(3)])
        new_space = (initial_space + dice_rolls) % 10
        return new_space

    def game_turn(self):
        self.player1_space = self.move_player(self.player1_space)
        self.player1_score += self.player1_space

        if self.player1_score >= self.WINNING_SCORE:
            return self.player2_score * self.die_rolls

        self.player2_space = self.move_player(self.player2_space)
        self.player2_score += self.player2_space

        if self.player2_score >= self.WINNING_SCORE:
            return self.player1_score * self.die_rolls

        return None

    def main(self):
        while True:
            score = self.game_turn()
            if score:
                return score


class QuantumGame:
    def __init__(self, filepath: str):
        _input = read_input(filepath)

        self.die = 1
        self.die_rolls = 0
        self.player1_space = int(_input[0].split(": ")[1])
        self.player2_space = int(_input[1].split(": ")[1])
        self.WINNING_SCORE = 21
        self.die_rolls = [
            x + y + z for x in range(1, 4) for y in range(1, 4) for z in range(1, 4)
        ]
        self.cache = {}

    def move_player(self, initial_space: int, dice: int):
        new_space = initial_space + dice

        if new_space % 10 == 0:
            new_space = 10
        elif new_space > 10 and new_space % 10 != 0:
            new_space = new_space % 10

        return new_space

    def play_game(
        self,
        player1_space: int,
        player1_score: int,
        player2_space: int,
        player2_score: int,
    ):
        # Check if this outcome is already in cache
        cache_key = (player1_space, player1_score, player2_space, player2_score)
        if cache_key in self.cache:
            return self.cache[cache_key]
        else:
            p1_wins = 0
            p2_wins = 0

            for d1 in self.die_rolls:
                new_player1_space = self.move_player(player1_space, d1)
                new_player1_score = player1_score + new_player1_space

                if new_player1_score >= self.WINNING_SCORE:
                    p1_wins += 1
                    continue

                for d2 in self.die_rolls:
                    new_player2_space = self.move_player(player2_space, d2)
                    new_player2_score = player2_score + new_player2_space

                    if new_player2_score >= self.WINNING_SCORE:
                        p2_wins += 1
                    else:
                        new_p1_wins, new_p2_wins = self.play_game(
                            new_player1_space,
                            new_player1_score,
                            new_player2_space,
                            new_player2_score,
                        )
                        p1_wins += new_p1_wins
                        p2_wins += new_p2_wins

            self.cache[cache_key] = p1_wins, p2_wins
            return p1_wins, p2_wins

    def main(self):
        player1_score = 0
        player2_score = 0
        p1_wins, p2_wins = self.play_game(
            self.player1_space, player1_score, self.player2_space, player2_score
        )
        return max(p1_wins, p2_wins)


@timer
def main(filepath: str):
    """
    Returns part 1 & 2 scores from a filepath.
    """
    part_1_score = Game(filepath).main()
    part_2_score = QuantumGame(filepath).main()
    return part_1_score, part_2_score


if __name__ == "__main__":
    part_1_score, part_2_score = main("aoc21.txt")
    print(f"PART 1: {part_1_score}")  # 757770
    print(f"PART 2: {part_2_score}")  # 712381680443927
