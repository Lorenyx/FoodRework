from dataclasses import dataclass, field
from os import read, write
from typing import List, Dict
import csv, re, json

RECIPEFILE = 'recipes.dat'
FOODFILE = 'food.csv'
TOOLS = json.load(open('tools.json', 'r'))

@dataclass
class FoodItem:
    id: str # exmaple:food_item
    oredict: list # Ore Dict key for categories
    recipe: list = field(init=False, repr=False) # Materials used to make item
    children: list = field(init=False, repr=False) # FoodItems that self can create
    hasWeight = False
    
    weight: float = 0.0

    def __post_init__(self):
        self.oredict = [f'ore:{ore}' for ore in self.oredict]
        self.recipe = self.getRecipe()
    

    def __str__(self):
        if self.materials:
            return f'{self.name} made with {len(self.materials)} mats'
        else:
            return f'{self.name} is basic'


    def isCooked(self):
        "Returns if item is cooked"
        for ore in self.oredict:
            if 'cook' in ore:
                return True
        return False


    def getRecipeValues(self):
        if self.id in RECIPEDICT.keys():
            return RECIPEDICT[self.id].materials.copy()
        return None

    
    def getRecipe(self):
        "Assigned to materials value"
        if self.id in RECIPEDICT.keys():
            return list(RECIPEDICT[self.id].materials.keys())
        if self.isCooked():
            self.setWeight(2.0)
        else:
            self.setWeight(1.0)
        return None


    def getValue(self, key):
        with open(FOODFILE, 'r') as f:
            readCSV = csv.DictReader(f, quotechar='"', fieldnames=FIELDNAMES)
            for row in readCSV:
                if row['Registry name'] == self.id:
                    return row[key]
            return None


    def setWeight(self, weight):
        "Assigns weight and changes bool"
        self.weight = weight
        self.hasWeight = True
        return self.weight


    def getWeight(self):
        ""
        if self.hasWeight:
            return self.weight

        weight = 0
        if self.isCooked():
            weight += 1

        for material in self.recipe:
            if isTool(material):
                weight += TOOLS[material]['weight']
                continue
            elif isOre(material):
                material = OREDICT[material][0]

            if FOODDICT[material].hasWeight:
                weight += FOODDICT[material].weight
            else:
                return None

        return self.setWeight(weight)


    def toCSV(self):
        return {
            'Registry name': self.id,
            'Weight': self.weight, 
            'Hunger': self.getValue('Hunger'), 
            'Saturation': self.getValue('Saturation'),
            'Display name': self.getValue('Display name'),
            'Ore Dict keys': self.oredict, 
            'Mod name': self.getValue('Mod name'), 
            'Item ID': self.getValue('Item ID'),
        }

@dataclass
class RecipeItem:
    name: str
    materials: dict # {Material name, count}



FIELDNAMES = ['Registry name', 'Hunger', 'Saturation', 'Meta/dmg', 'Display name', 'Ore Dict keys', 'Mod name', 'Item ID', 'Subtypes']
NEWFIELDNAMES = ['Registry name',
                'Weight',
                'Hunger',
                'Saturation',
                'Display name',
                'Ore Dict keys',
                'Mod name',
                'Item ID'
                ]
FOODDICT = {} # FIlled with FoodItems
RECIPEDICT = {}
OREDICT = {'gemAmbrosium': ['aether_legacy:ambrosium_shard']}
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


def isFood(name):
    "Returns if recipe name is a food item"
    with open(FOODFILE) as f:
        if '<' in name:
            name = name[1:-1]
        for line in f:
            if name == line.split(',')[0]:
                return True
        return False
            
            
def isOre(key: str):
    "Returns if name (id) is an ore"
    if key.startswith('ore:'):
        return OREDICT[key]
    return None


def isTool(key: str):
    "Returns weight if tool else None"
    if key in TOOLS:
        return TOOLS[key]['weight']
    return None


def updateOres(foodID, weight):
    if FOODDICT[foodID].oredict:
        for ore in FOODDICT[foodID].oredict:
            for food in OREDICT[ore]:
                FOODDICT[food].weight = weight


def cleanID(foodID: str):
    "Turns string into clean, standard format of mod_name:registry_name"
    if '<' in foodID:
        foodID = foodID[1:-1] # removes < and > from ends
    if len(foodID.split(':')) > 2:
        foodID = foodID[:foodID.rindex(':')]
    return foodID
     

def FillRecipeDict():
    "Pulls lines from RECIPEFILE and converts them to more accessible format"
    print('[=] Filling Recipes...')
    with open(RECIPEFILE) as r:
        linecount = 0
        for line in r:
            linecount += 1
            # Sorry the below line does a lot of python magic but it works so...
            words = re.findall('<(.*?)>', "".join(line.split()))
            if len(words) > 1:
                # dict = {'name': f'<{words[0]}>', 'mats': {f'<{i}>': words[1:].count(i) for i in words[1:]}}
                recipe = RecipeItem(name=words[0], materials={
                    cleanID(item): words[1:].count(item) for item in words[1:]})
                
                if isFood(recipe.name) and all([mat not in SKIPPED for mat in recipe.materials ]):
                    RECIPEDICT[recipe.name] = recipe


def FillFoodDict():
    if len(RECIPEDICT) == 0:
        FillRecipeDict()
    print('[=] Filling Food Dict...')
    with open(FOODFILE, 'r') as f:
        readCSV = csv.DictReader(f, quotechar='"', fieldnames=FIELDNAMES)
        for row in readCSV:
            #Registry name,Hunger,Saturation,Meta/dmg,Display name,Ore Dict keys,Mod name,Item ID,Subtypes
            food = FoodItem(
                id = row['Registry name'],
                oredict = row['Ore Dict keys'].replace(' ', '').split(','),
            )
            FOODDICT[food.id] = food

            #Cause FUCK ambrosium
            if food.id == 'aether_legacy:ambrosium_shard':
                food.step=0
            # Updates OREDICT to include every food under oredict key
            if not food.oredict[0].isspace():
                for ore in food.oredict:
                    if ore in OREDICT.keys():
                        OREDICT[ore].append(f'{food.id}')
                    else:
                        OREDICT[ore]=[food.id]
            else:
                food.oredict = None


def genWeights():
    "Generates weight values for food items"
    from collections import deque
    queue = deque(FOODDICT.values())
    print('[=] Generating weights...')
    while len(queue): # Continue until empty
        # if len(queue) == 2:
        #     print(queue)
        #     break
        food = queue.popleft()
        
        if not food.getWeight():
            queue.append(food)


def writeFoods():
    "Writes all food into CSV file"
    print('[=] Saving Foods...')
    with open('updatedFood.csv', 'w', newline='') as f:
        writeCSV = csv.DictWriter(f, fieldnames=NEWFIELDNAMES, quotechar='"')
        writeCSV.writeheader()
        for food in FOODDICT.values():
            writeCSV.writerow(food.toCSV())




def run():
    FillRecipeDict()
    FillFoodDict()
    genWeights()
    writeFoods()


if __name__ == '__main__':
    
    run()
    print(FOODDICT['harvestcraft:lycheeteaitem'].weight)
