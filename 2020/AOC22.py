''' Pretty straightforward problem. The changed rules in part 2 require
a new play_round function that can call on play_recursive_game. 

Part 1 is quick, part 2 is slow (but probably under a minute).'''

def parse_input(_input):
    player1 = _input.split('\n\n')[0].replace('Player 1:\n', '').split('\n')
    player2 = _input.split('\n\n')[1].replace('Player 2:\n', '').split('\n')

    player1 = [int(c) for c in player1]
    player2 = [int(c) for c in player2]

    return player1, player2

def play_round(player1, player2):
    topcard1 = player1[0]
    topcard2 = player2[0]

    player1.pop(0)
    player2.pop(0)

    if topcard1 > topcard2:
        player1.append(topcard1)
        player1.append(topcard2)
    else:
        player2.append(topcard2)
        player2.append(topcard1)
        
    return player1, player2

def get_score(_input):
    player1, player2 = parse_input(_input)

    while len(player1) > 0 and len(player2) > 0:
        player1, player2 = play_round(player1, player2)

    winner = player1 if len(player1) > 0 else player2
    score = sum([v * (len(winner) - ix) for ix,v in enumerate(winner)])

    return score

def play_recursive_round(player1, player2, past_plays): 
    '''Initially a bit buggy before realized that the lists
    stored in past_plays are affected by subsequent changes
    to the hands of players 1 & 2. Solution is to append a
    shallow copy of the lists instead. '''
    
    # Check if this ever happened before
    if player1 in past_plays['player1'] and player2 in past_plays['player2']:
        return player1, [], past_plays
    else:        
        # Update past plays
        past_plays['player1'].append(player1.copy())
        past_plays['player2'].append(player2.copy())
        
        # Get top cards
        topcard1 = player1[0]
        topcard2 = player2[0]

        player1.pop(0)
        player2.pop(0)
        
        # Recursive Game
        if len(player1) >= topcard1 and len(player2) >= topcard2:
            # Copy Decks
            new_player1 = player1[:topcard1].copy()
            new_player2 = player2[:topcard2].copy()
            
            # Recursion
            winner, winner_bool = play_recursive_game(new_player1, new_player2)
            
        # Regular Game
        else:
            winner_bool = 1 if topcard1 > topcard2 else 0
        
        # Change Decks
        if winner_bool == 1:
            player1.append(topcard1)
            player1.append(topcard2)
        else:
            player2.append(topcard2)
            player2.append(topcard1)

        return player1, player2, past_plays

def play_recursive_game(player1, player2):
    past_plays = {'player1': [], 'player2': []}
    
    while len(player1) > 0 and len(player2) > 0:
        player1, player2, past_plays = play_recursive_round(player1, player2, past_plays)

    winner = player1 if len(player1) > 0 else player2
    winner_bool = 1 if len(player1) > 0 else 0

    return winner, winner_bool

def get_recursive_score(_input):
    player1, player2 = parse_input(_input)

    winner, winner_bool = play_recursive_game(player1, player2)

    score = sum([v * (len(winner) - ix) for ix,v in enumerate(winner)])

    return score
 
if __name__ == "__main__":
    _input = open("aoc_22.txt").read()
    
    print("PART 1")
    score = get_score(_input) # 31455
    print(score)
    print("")
    print("PART 2")
    score = get_recursive_score(_input) # 32528
    print(score)
