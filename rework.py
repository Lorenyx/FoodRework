from dataclasses import dataclass, field
from typing import List, Dict
import csv, re

RECIPEFILE = 'recipes.dat'
FOODFILE = 'food.csv'

@dataclass
class FoodItem:
    weight: float = field(init=False, repr=False) 
    name: str # Name of the food item e.g. "Fluffy Wheat"
    oredict: list # Ore Dict key for categories

    materials: list = field(init=False, repr=False) 
    cooked: bool = field(init=False, repr=False)
    mod: str  # Name of parent mod
    id: str # Game ID of food e.g. example:fluffy_wheat
    
    hunger: int = 0
    saturation: float = 0.0

    step: int = -1

    def __post_init__(self):
        self.weight = self.getWeight()
        self.materials = self.getMaterials()
        self.cooked = self.isCooked()

    
    def __str__(self):
        if self.materials:
            return f'{self.name} made with {len(self.materials)} mats'
        else:
            return f'{self.name} is basic'

    
    def toCSV(self):
        "Writes data in CSV format"
        pass

    def isCooked(self):
        "Returns if item is cooked"
        for ore in self.oredict:
            if 'cook' in ore:
                return True
        return False

    def isBasic(self):
        "Returns if food is crop, raw meat, or other non-crafted fooditem"
        return self.materials == None


    def getMaterialDict(self):
        if self.id in RECIPEDICT.keys():
            return RECIPEDICT[self.id].materials.copy()
        return None

    
    def getMaterials(self):
        "Assigned to materials value"
        if self.id in RECIPEDICT.keys():
            return list(RECIPEDICT[self.id].materials.keys())
        self.step = 0
        return None


    def getWeight(self):
        #TODO Calculate weight of item using Calamari method in TODO.txt
        return None

    


@dataclass
class RecipeItem:
    name: str
    materials: dict # {Material name, count}


FOODDICT = {} # FIlled with FoodItems
RECIPEDICT = {}
OREDICT = {'gemAmbrosium': ['aether_legacy:ambrosium_shard']}
FIELDNAMES = ['Registry name', 'Hunger', 'Saturation', 'Meta/dmg', 'Display name', 'Ore Dict keys', 'Mod name', 'Item ID', 'Subtypes']


def isFood(name):
    "Returns if recipe name is a food item"
    with open(FOODFILE) as f:
        if '<' in name:
            name = name[1:-1]
        for line in f:
            if name == line.split(',')[0]:
                return True
        return False
            

def FillFoodDict():
    if len(RECIPEDICT) == 0:
        FillRecipeDict()

    with open(FOODFILE, 'r') as f:
        readCSV = csv.DictReader(f, quotechar='"', fieldnames=FIELDNAMES)
        for row in readCSV:
            #Registry name,Hunger,Saturation,Meta/dmg,Display name,Ore Dict keys,Mod name,Item ID,Subtypes
            food = FoodItem(
                id = row['Registry name'],
                hunger = row['Hunger'],
                saturation = row['Saturation'],
                name = row['Display name'],
                oredict = row['Ore Dict keys'].split(','),
                mod = row['Mod name'],
            )
            FOODDICT[food.id] = food

            #Cause FUCK ambrosium
            if food.id == 'aether_legacy:ambrosium_shard':
                food.step=0
            if food.oredict and food.oredict[0] != '':
                for ore in food.oredict:
                    if ore in OREDICT.keys():
                        OREDICT[ore].append(food.id)
                    else:
                        OREDICT[ore]=[food.id]


def FillRecipeDict():
    "Pulls lines from RECIPEFILE and converts them to more accessible format"
    
    with open(RECIPEFILE) as r:
        linecount=0
        for line in r:
            linecount+=1
            # Sorry the below line does a lot of python magic but it works so...
            words = re.findall('<(.*?)>', "".join(line.split()))
            if len(words) > 1:
                # dict = {'name': f'<{words[0]}>', 'mats': {f'<{i}>': words[1:].count(i) for i in words[1:]}}
                recipe = RecipeItem(name=words[0], materials={item: words[1:].count(item) for item in words[1:]})

                if isFood(recipe.name):
                    RECIPEDICT[recipe.name] = recipe


def calcSteps():
    "Calculates how many steps required to craft item."
    from collections import deque
    deck = deque(FOODDICT.values())
    step = 0

    while len(deck) > 0:
        food = deck.popleft()
        if food.id == 'aether_legacy:ambrosium_shard':
            continue
        doBreak = False
        if food.materials == None:
            continue

        highestStep = 0
        for matName in food.materials:
            if matName == 'null':
                continue
            if isFood(matName):
                mat = FOODDICT[matName]
                if mat.step == -1:
                    doBreak = True
                    break
                elif mat.step > highestStep:
                 highestStep = mat.step+1
            
            elif highestStep == 0:
                highestStep=1

        if doBreak:
            deck.append(food)
        else:
            food.step = highestStep
            for ore in food.oredict:
                updateOres(ore, food.step)


def updateOres(orename, step):
    if orename:
        for food in OREDICT[orename]:
            FOODDICT[food].step = step


if __name__ == '__main__':
    FillFoodDict()
    calcSteps()
    for food in FOODDICT.values():
        
