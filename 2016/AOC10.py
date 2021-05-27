def add_to_dict_list(d, key, obj):
    if key in d.keys():
        d[key].append(obj)
    else:
        d[key] = [obj]

def process_input(instructions):
    chips_repo = {}
    bot_instructions = {}

    for line in instructions:
        if 'goes to' in line:
            val, bot = line.replace('value ', '').split(' goes to ')
            val = int(val)
            add_to_dict_list(chips_repo, bot, val)
        else:
            bot, line = line.split(' gives low to ')
            low_recip, high_recip = line.split(' and high to ')

            add_to_dict_list(bot_instructions, bot, low_recip)
            add_to_dict_list(bot_instructions, bot, high_recip)

    return chips_repo, bot_instructions

def activate_bots(chips_repo, bot_instructions, part):
    active_bots = [bot for bot, chips in chips_repo.items() if len(chips) >= 2]

    while active_bots:
        for bot in active_bots:
            chips = chips_repo[bot]
            low_recip, high_recip = bot_instructions[bot]
            low_chip, high_chip = min(chips), max(chips)

            if low_chip == 17 and high_chip == 61 and part == 1:
                return bot

            add_to_dict_list(chips_repo, low_recip, low_chip)
            add_to_dict_list(chips_repo, high_recip, high_chip)

            chips_repo[bot] = []

        active_bots = [bot for bot, chips in chips_repo.items() if len(chips) >= 2]

    return chips_repo

if __name__ == '__main__':
    instructions = open("2016/aoc10.txt").read().splitlines()

    chips_repo, bot_instructions = process_input(instructions)
    sol1 = activate_bots(chips_repo, bot_instructions, part=1)  # 116
    print(f'PART 1: {sol1}')

    chips_repo = activate_bots(chips_repo, bot_instructions, part=2)
    sol2 = chips_repo['output 0'][0] * chips_repo['output 1'][0] * chips_repo['output 2'][0]  # 23903
    print(f'PART 2: {sol2}')
