class MarbleGame():
    def __init__(self, n_marbles, n_players, current_marble, current_player, circle, score):
        self.n_players = n_players
        self.n_marbles = n_marbles
        self.current_marble = current_marble
        self.current_player = current_player
        self.circle = circle
        self.score = score

    def print_circle(self):
        marble = 0
        _output = [str(marble)]

        while self.circle[marble][0] != 0:
            marble = self.circle[marble][0]
            _output.append(str(marble))

        return ' '.join(_output)

    def move_countercw(self, n_moves):
        prev_marble = self.current_marble

        for r in range(n_moves):
            prev_marble = self.circle[prev_marble][1]
            
        return prev_marble

    def add_marble(self, new_marble):
        next_marble = self.circle[self.current_marble][0]
        prev_marble_cw, prev_marble_counter_cw = self.circle[next_marble]

        self.circle[new_marble] = [prev_marble_cw, next_marble]
        self.circle[next_marble][0] = new_marble
        self.circle[prev_marble_cw][1] = new_marble

        self.current_marble = new_marble

    def remove_marble(self, removable_marble, new_marble):
        # Find marble data
        prev_marble_cw, prev_marble_counter_cw = self.circle[removable_marble]

        # Remove prev marble
        self.circle[prev_marble_cw][1] = prev_marble_counter_cw
        self.circle[prev_marble_counter_cw][0] = prev_marble_cw

        # Adjust score + current marble
        self.score[self.current_player] += new_marble + removable_marble
        self.current_marble = prev_marble_cw

def play_game(n_marbles, n_players):
    current_marble = 0
    current_player = 0
    circle = {0: [0, 0]}
    score = {p:0 for p in range(n_players)}

    game = MarbleGame(n_marbles, n_players, current_marble, current_player, circle, score)

    for new_marble in range(1, n_marbles):
        if new_marble % 23 != 0:
            game.add_marble(new_marble)
        else:
            prev_marble = game.move_countercw(7)
            game.remove_marble(prev_marble, new_marble)

        game.current_player = (game.current_player + 1) % n_players

    return max(list(game.score.values()))

if __name__ == "__main__":
    score1 = play_game(71843, 468) # 385820
    score2 = play_game(100 * 71843, 468) # 3156297594

    print('PART 1: {} \n PART 2: {}'.format(score1, score2))
