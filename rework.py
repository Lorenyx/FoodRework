from dataclasses import dataclass, field
from os import read, write
from typing import List, Dict
import csv, re, json

RECIPEFILE = 'recipes.dat'
FOODFILE = 'weightedFood.csv'
TOOLS = json.load(open('tools.json', 'r'))

@dataclass
class FoodItem:
    id: str # exmaple:food_item
    oredict: list # Ore Dict key for categories
    recipe: list = field(init=False, repr=False) # Materials used to make item
    children: list = field(init=False, repr=False) # FoodItems that self can create
    hasWeight = False
    
    weight: float = 0.0
    product: int = 1

    def __post_init__(self):
        #TODO Verify that this is backwards compatible
        if not self.oredict:
            self.oredict = [f'ore:{ore}' for ore in self.oredict]
        self.recipe = self.getRecipe()
    

    def __str__(self):
        if self.recipe:
            return f'{self.id} made with {len(self.recipe)} mats'
        else:
            return f'{self.id} is basic'


    def isCooked(self):
        "Returns if item is cooked"
        if 'Cooked' in self.getValue('Display name'):
            return True
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
            recipe = RECIPEDICT[self.id]
            self.product = recipe.product
            return list(recipe.materials.keys())
        self.setWeight() 
        return None


    def getValue(self, key):
        with open(FOODFILE, 'r') as f:
            readCSV = csv.DictReader(f, quotechar='"', fieldnames=NEWFIELDNAMES)
            for row in readCSV:
                if row['Registry name'] == self.id:
                    return row[key]
            return None


    def setWeight(self, weight=1.0):
        "Assigns weight and changes bool"
        if self.isCooked(): 
            weight+=1  # Weight of being cooked
        self.weight = int(weight)
        self.hasWeight = True
        return self.weight


    def getWeight(self):
        ""
        if self.hasWeight:
            return self.weight

        weight = 0
        if self.isCooked():
            weight += 1

        matDict = self.getRecipeValues()
        for material in self.recipe:
            try:
                if isTool(material):
                    weight += TOOLS[material]['weight']
                elif isOre(material):
                    if FOODDICT[OREDICT[material][0]].hasWeight:
                        weight += FOODDICT[OREDICT[material][0]].weight * matDict[material]
                    else: 
                        return None
                elif FOODDICT[material].hasWeight:
                    weight += FOODDICT[material].weight * matDict[material]
                
                else:
                    return None
            except KeyError:
                print(f'[-] No key: {material}')

        return self.setWeight(weight)


    def makeValues(self):
        "Returns tuple of (Hunger, SaturationModifier)"
        if self.id in SPECIALFOODS:
            return (self.getValue('Hunger'), self.getValue('Saturation'))
        weight = int(float(self.weight.strip()))
        if weight == 1: # Morsels (no saturation)
            return (1,0.0)
        if weight <= 3: # Snacks (between 2-3 steps) (saturation half chunk)
            return (2, 0.125) # Sat = 0.5
        if weight <= 5: # Light Meal (between 4-5 steps) (saturation one less)
            return (5, .15)
        if weight <= 8: # Meal (between 6-8 steps) (saturation equal)
            return (7, .2)
        if weight <= 11: # Large Meal (Between 9-11 steps) (Saturation greater)
            return (9, .4)
        else:
            return (weight, .5)


    def toCSV(self):
        hunger, saturationModifier = self.makeValues()
        return {
            'Registry name': self.id,
            'Weight': self.weight, 
            'Product': self.product,
            'Hunger': hunger, 
            'Saturation': saturationModifier*2*hunger,
            'Display name': self.getValue('Display name'),
            'Ore Dict keys': self.oredict, 
            'Mod name': self.getValue('Mod name'), 
            'Item ID': self.getValue('Item ID'),
        }

    def toJson(self):
        return {
            'name':self.id,
            'hunger': self.makeValues()[0],
            'saturationModifier': self.makeValues()[1]
            }

    def fromCSV(csvDict):
        food = FoodItem(
            id=csvDict['Registry name'],
            product=csvDict['Product'],
            oredict=csvDict['Ore Dict keys']
        )
        food.weight = csvDict['Weight']
        food.hasWeight = True

        return food
        

@dataclass
class RecipeItem:
    name: str
    materials: dict # {Material name, count}
    product: int = 1


FIELDNAMES = ["Mod name", "Registry name", "Item ID", "Meta/dmg",
              "Subtypes", "Display name", "Hunger", "Saturation", "Ore Dict keys"]
NEWFIELDNAMES = ['Registry name',
                'Weight',
                'Product',
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
SPECIALFOODS = []

def isFood(name):
    "Returns if recipe name is a food item"
    with open(FOODFILE) as f:
        if '<' in name:
            name = name[1:-1]
        for line in f:
            if name == line.split(',')[1].replace('"', ''):
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
                recipe = RecipeItem(name=words[0], materials={cleanID(item): words[1:].count(item) for item in words[1:]})
                if isFood(recipe.name) and all([mat not in SKIPPED for mat in recipe.materials ]):
                    ls = line.split(', ', maxsplit=2)
                    if len(ls) > 1 and '*' in ls[1]:
                        recipe.product = int(ls[1][ls[1].index('*')+2:])
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
                oredict = row['Ore Dict keys'].split(','), 
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


def FillNewFoodDict():
    print('[=] Adding weighted foods')
    with open('weightedFood.csv', 'r') as f:
        readCSV = csv.DictReader(f, quotechar='"', fieldnames=NEWFIELDNAMES)
        for row in readCSV:
            food = FoodItem.fromCSV(row)
            FOODDICT[food.id] = food


def genWeights():
    "Generates weight values for food items"
    from collections import deque
    queue = deque(FOODDICT.values())
    print('[=] Generating weights...')
    while len(queue): # Continue until empty
        food = queue.popleft()
        
        if not food.getWeight():
            queue.append(food)


def writeFoods():
    "Writes all food into CSV file"
    print('[=] Saving Foods...')
    with open('weightedFood.csv', 'w', newline='') as f:
        writeCSV = csv.DictWriter(f, fieldnames=NEWFIELDNAMES, quotechar='"')
        writeCSV.writeheader()
        for food in FOODDICT.values():
            writeCSV.writerow(food.toCSV())


def writeNewFoods():
    "Writes all food into CSV file"
    print('[=] Saving Foods...')
    with open('newValueFood.csv', 'w', newline='') as f:
        writeCSV = csv.DictWriter(f, fieldnames=NEWFIELDNAMES, quotechar='"')
        writeCSV.writeheader()
        for food in FOODDICT.values():
            writeCSV.writerow(food.toCSV())


def writeFoodOverride():
    print('[=] Writing Override json...')
    with open('foodOverrides.json', 'w') as j:
        writeList = [food.toJson() for food in FOODDICT.values()]
        json.dump({'foods':writeList[1:]}, j, indent=4)
        

def run():
    FillRecipeDict()
    FillNewFoodDict()
    writeFoodOverride()
    # FillFoodDict()
    # genWeights()
    # writeFoods()


if __name__ == '__main__':
    
    run()
    
