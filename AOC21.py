import re

def parse_input(_input):
    ''' Takes input, returns a list of sets of ingredients 
    and a list of allergens per food.

    OUTPUT
    allergens: list of allergens per food.
        -> EX: [['dairy', 'fish'], ['dairy'], ['soy'], ['fish']]
    ingredients: list of sets of ingredients per food.
        -> EX: [{'kfcds', 'mxmxvkd', 'nhms', 'sqjhc'},
                 {'fvjkl', 'mxmxvkd', 'sbzzf', 'trh'},
                 {'fvjkl', 'sqjhc'},
                 {'mxmxvkd', 'sbzzf', 'sqjhc'}]
    flat_ingredients: list of ingredients in order of appearance.
    '''
    # Get List of Ingredients
    ingredients = re.sub(' \(.*?\)', '', _input).splitlines()
    ingredients = [set(i.split(' ')) for i in ingredients]
    
    # Get Flat List of Ingredients
    flat_ingredients = re.sub(' \(.*?\)', '', _input)
    flat_ingredients = flat_ingredients.replace('\n', ' ').split(' ')

    # Get Allergens
    allergens = re.findall('\(.*?\)', _input)
    allergens = [a.replace('(contains ', '').replace(')', '') for a in allergens]
    allergens = [a.split(', ') for a in allergens]

    return ingredients, flat_ingredients, allergens

def find_non_allergens(_input):
    ''' Find ingredients that may be allergens.'''

    # Parse Input
    ingredients, flat_ingredients, allergens = parse_input(_input)

    # Get all Alergens
    arllergen_list = set([a for sublist in allergens for a in sublist])

    # Adds Ingredients that are linked to allergen
    allergen_mapping = {a:[] for a in arllergen_list}

    for ix, v in enumerate(allergens):
        for a in v:
            allergen_mapping[a].append(ingredients[ix])

    # Find Intersection of Ingredients per Allergen
    allergen_mapping = {a:set.intersection(*allergen_mapping[a]) for a in arllergen_list}
    suspects = list(allergen_mapping.values())
    suspects = list(set.union(*suspects))

    # Get Non Allergens
    non_allergens = set(flat_ingredients).difference(suspects)

    # Count their appearance
    result = 0

    for ing in non_allergens: 
        result += sum([1 for i in flat_ingredients if i == ing])

    return result, allergen_mapping

def process_of_elimination(elimination_dict):
    '''Reusing this function from Day 16.

    Takes dict and goes through an iterative elimination process.
    When a field only has 1 possible position left, the field is added to
    correct_mapping and that position is removed from the possible positions
    of all other fields. This continues until elimination_dict is empty, i.e.,
    all fields have been matched.
    PARAMETERS:
    elimination_dict = {'field_a': [positions field_a could be in]}
        -> EX. {'class': [1, 2], 'row': [0, 1, 2], 'seat': [2]}
    RETURNS:
    correct_mapping = {'field_a': [position field a is in]}
        -> EX. {'class': 1, 'row': 0, 'seat': 2}
    '''
    correct_mapping = {}
    elimination_dict = {k:list(v) for k,v in elimination_dict.items()}

    while elimination_dict:
        initial_key = [k for k,v in elimination_dict.items() if len(v) == 1]
        key = initial_key[0]

        correct_pos = elimination_dict[key][0]
        correct_mapping[key] = correct_pos
        del elimination_dict[key]

        for other_key in elimination_dict:
            if correct_pos in elimination_dict[other_key]:
                elimination_dict[other_key].remove(correct_pos)

    return correct_mapping

def get_mappings(allergen_mapping):
    # Match ingredients to allergens
    correct_mapping = process_of_elimination(elimination_dict)

    # Getting result as specified 
    # w some extra logic for getting the ingredients in right order
    order_keys = list(correct_mapping.keys())
    order_keys.sort()

    result = []

    for k in order_keys:
        result.append(correct_mapping[k])

    return ','.join(result)
 
if __name__ == "__main__":
    _input = open("aoc_21.txt").read()
    
    print("PART 1")
    result, allergen_mapping = find_non_allergens(_input) 
    print(result) # 2072
    print("")
    print("PART 2")
    get_mappings(allergen_mapping) # fdsfpg,jmvxx,lkv,cbzcgvc,kfgln,pqqks,pqrvc,lclnj


