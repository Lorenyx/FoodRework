from collections import deque
import json


def init():
    global RECIPEFILE
    RECIPEFILE = 'recipes.dat'

    global FOODCSV
    FOODCSV = 'weightedFood.csv'

    global SPECIALFOODS
    SPECIALFOODS = ['rats:confit_byaldi']

    global FIELDNAMES
    FIELDNAMES = [
        'Registry name',
        'Weight',
        'Product',
        'Hunger',
        'Saturation',
        'Display name',
        'Ore Dict keys',
        'Mod name',
        'Item ID'
    ]

    global OREDICT
    OREDICT = {}


    from .FoodItem import FoodItem
    global FOODDICT
    FOODDICT = {}
    print(f'[=] Parsing {FOODCSV} ...')
    import csv
    with open(FOODCSV, 'r') as f:
        readCSV = csv.DictReader(f, quotechar='"', fieldnames=FIELDNAMES)
        for row in readCSV:
            food = FoodItem.fromCSV(row)
            FOODDICT[food.id] = food

            for ore in food.oredict:
                if ore in OREDICT:
                    OREDICT[ore].append(food.id)
                else:
                    OREDICT[ore]=[food.id]


    from .RecipeItem import RecipeItem
    global RECIPEDICT
    RECIPEDICT = {}
    print('[=] Filling Recipe Book ...')
    import re
    with open(RECIPEFILE) as r:
        for line in r:
            words = re.findall('<(.*?)>', "".join(line.split()))
            if len(words) and words[0] in FOODDICT:
                recipe = RecipeItem(
                    name = words[0],
                    recipe = [item for item in words[1:]]
                )
                
                ls = line.split(', ', maxsplit=2)
                if len(ls) > 1 and '*' in ls[1]:
                    recipe.product = int(ls[1][ls[1].index('*')+2:])

                RECIPEDICT[recipe.name] = recipe
            

    for recipe in RECIPEDICT.values():
        recipe.generateFoods()

    # Generate Recipe
    for food in FOODDICT.values():
        food.generateRecipe()
        # if food.recipe:   
        #     print(food.recipe.foods)

    # Generate Weights
    queue = deque(FOODDICT.values())
    print('[=] Generating weights...')
    while len(queue):  # Continue until empty
        print(len(queue))
        food = queue.popleft()
        value = food.generateWeight()
        if not value:
            queue.append(food)

        if len(queue) == 305:
            for x in queue:
                print(x.recipe)
            # print(queue)
            break


    print('[=] Writing Override json...')
    with open('foodOverride.json', 'w') as j:
        writeList = [food.toJson() for food in FOODDICT.values()]
        json.dump({'foods': writeList[1:]}, j, indent=4)


    global TOOLS
    TOOLS = json.load(open('tools.json', 'r'))
    
    
    global SKIPPED
    SKIPPED = [ # fuck cheese wheels
        'aether_legacy:ambrosium_block',
        'charm:rotten_flesh_block',
        'minecraft:melon_block',
        'animania:friesian_cheese_wheel',
        'animania:goat_cheese_wheel', 
        'animania:holstein_cheese_wheel', 
        'animania:jersey_cheese_wheel',
        'animania:sheep_cheese_wheel'
        ]
    
