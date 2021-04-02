import re

def parse_input(_input):
    k = _input.split(' contain ')[0].replace(' bags', '') # key
    v = _input.split(' contain ')[1].split(', ') # value, list

    v = [re.sub('( bags?)|(\d+ )|(\.)', '', s) for s in v]

    if 'no other' in v:
        v = []

    return k, v

def parse_numerical_input(_input):
    k = _input.split(' contain ')[0].replace(' bags', '') # key
    v = _input.split(' contain ')[1].split(', ') # value, list

    v = [re.sub('[^\\d]', '', s) for s in v]

    if '' in v:
        v = []
    else:
        v = [int(i) for i in v]

    return k, v

def find_compliant_bags(_input):
    # Start by the 1st layer of bags that can hold our 'shiny gold' bag
    is_new_container = True
    containers = [k for k,v in _input.items() if 'shiny gold' in v]
    all_containers = containers

    # Keep going to find bags that find bags that hold etc. until no new bags
    while is_new_container == True:
        new_containers = []
        n = len(containers)
        i = 0

        for c in containers:
            temp_containers = [k for k,v in _input.items() if c in v]
            
            if temp_containers:
                new_containers = temp_containers + new_containers 
                all_containers = temp_containers + all_containers
            else:
                i += 1

        # None of the new bags had a bag that could hold them
        if i == n:
            is_new_container = False
        else:
            containers = new_containers

    return len(set(all_containers))

def count_held_bags(rules_input, bag_count):
    # Start by the 1st layer of bags held by our 'shiny gold' bag
    total = 0
    is_new_contained = True
    
    contained_bags = rules_input['shiny gold']
    all_contained = contained_bags
    
    n_contained_bags = bag_count['shiny gold']

    # Keep going to find bags that find bags that are held by etc. until no new bags
    while is_new_contained == True:        
        new_contained = []
        new_n_contained = []
        n = len(contained_bags)
        empty_counter = 0

        for i,c in enumerate(contained_bags):
            temp_contained = rules_input[c]
            temp_n_contained = list(n_contained_bags[i] * np.array(bag_count[c]))
            total += n_contained_bags[i]
            
            if temp_contained:
                new_contained = new_contained + temp_contained
                all_contained = all_contained + temp_contained
                new_n_contained = new_n_contained + temp_n_contained
            else:
                empty_counter += 1

        # None of the new bags had a bag that could hold them
        if empty_counter == n:
            is_new_contained = False
        else:
            contained_bags = new_contained
            n_contained_bags = new_n_contained

    return total


if __name__ == "__main__":
    _input = open("aoc_7.txt").read().splitlines()
    
    print("PART 1")
    all_rules = dict(map(parse_input, test))
    find_compliant_bags(all_rules)

    print("")
    print("PART 2")
    bag_count = dict(map(parse_numerical_input, _input))
    count_held_bags(all_rules, bag_count)