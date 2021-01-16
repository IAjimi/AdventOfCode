def password_validity_check(string):
    rules = string.split(':')[0]
    password = string.split(':')[1]
    
    letter = rules.split(' ')[1]
    _min = rules.split(' ')[0].split('-')[0]
    _max = rules.split(' ')[0].split('-')[1]
    _min, _max = int(_min), int(_max)
    
    if (password.count(letter) >= _min) and (password.count(letter) <= _max):
        return 1
    else:
        return 0

def new_password_validity_check(string):
    rules = string.split(': ')[0]
    password = string.split(': ')[1]
    
    letter = rules.split(' ')[1]
    _min = rules.split(' ')[0].split('-')[0]
    _max = rules.split(' ')[0].split('-')[1]
    _min, _max = int(_min) - 1, int(_max) - 1 # need to match position numbering of prompt
    
    if (password[_min] == letter) and (password[_max] == letter):
        return 0
    elif (password[_min] != letter) and (password[_max] != letter):
        return 0
    else:
        return 1

if __name__ == "__main__":
    _input = open("aoc_2.txt").read().splitlines()
    
    print("PART 1")
    sum(list(map(password_validity_check, _input)))
    print("")
    print("PART 2")
    sum(list(map(new_password_validity_check, _input)))