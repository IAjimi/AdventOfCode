from operator import itemgetter

def check_passport_fields(passport):
    passport_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    validity_check = [1 if field in passport else 0 for field in passport_fields]
    
    if sum(validity_check) == 7:
        return 1
    else:
        return 0

def find_valid_passports(_input):
    '''Narrow down input to passports that have all the fields - not actually used here'''
    valid_passports = list(map(check_passport_fields, _input))
    valid_passports = [i for i,e in enumerate(valid_passports) if e == 1]
    remaining_passports = list(itemgetter(*valid_passports)(_input))
    return remaining_passports

def check_passport_values(passport):
    processed_passport = passport.split(' ')
    score = 0

    for field_entry in processed_passport:
        field = field_entry.split(':')[0]
        val = field_entry.split(':')[1]
        numbers = sum(c.isdigit() for c in val)

        if field == 'byr':
            if numbers == 4 and int(val) >= 1920 and int(val) <= 2002:
                score += 1
            else:
                return 0 # uses return to end function execution as soon as we know passport won't be valid

        if field == 'iyr':
            if numbers == 4 and int(val) >= 2010 and int(val) <= 2020:
                score += 1
            else:
                return 0

        if field == 'eyr':
            if numbers == 4 and int(val) >= 2020 and int(val) <= 2030:
                score += 1
            else:
                return 0

        if field == 'hgt':
            measure = val[-2:]
            height = val[:-2]

            if measure == 'cm' and int(height) >= 150 and int(height) <= 193:
                score += 1
            elif measure == 'in' and int(height) >= 59 and int(height) <= 76:
                score += 1
            else:
                return 0

        if field == 'hcl':
            if val[0] != '#':
                return 0
            else:
                valid_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
                valid_character_count = [1 if l in valid_characters else 0 for l in val]

                if sum(valid_character_count) == 6:
                    score += 1
                else:
                    return 0

        if field == 'ecl':
            correct_values = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

            if val in correct_values:
                score += 1
            else:
                return 0

        if field == 'pid':
            if numbers == 9:
                score += 1
            else:
                return 0

    return score


if __name__ == "__main__":
    _input = open("aoc_4.txt").read()
    _input = [i.replace('\n', ' ') for i in _input.split('\n\n')] # split by passport (double break) & clean input
    
    print("PART 1")
    sum(list(map(check_passport_fields, _input)))
    print("")
    print("PART 2")
    valid_passports = [1 if check_passport_values(p) == 7 else 0 for p in _input]
    sum(valid_passports)