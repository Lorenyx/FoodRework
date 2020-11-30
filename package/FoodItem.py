from dataclasses import dataclass, field
import csv, json, re

from .RecipeItem import RecipeItem
from . import settings

FOODCSV = settings.FOODCSV
FIELDNAMES = settings.FIELDNAMES
SPECIALFOODS = settings.SPECIALFOODS
OREDICT = settings.OREDICT


@dataclass
class FoodItem:
    id: str # exmaple:food_item
    hunger: int
    saturation: float # (SM * 2 * H)
    oredict: list # Ore Dict key for categories
    recipe: RecipeItem = None # Materials used to make item
    
    weight: float = 0.0
    product: int = 1


    def __post_init__(self):
        # self.oredict = [f'ore:{ore}' for ore in self.oredict if ':' not in ore]
        if type(self.oredict) == str:
            self.oredict = re.findall('\'(.*?)\'', "".join(self.oredict.split()))
        if 'ore:' in self.oredict:
            self.oredict.remove('ore:')
        pass


    def __str__(self):
        print(self.id)


    def __repr__(self):
        print(self.id)

        
    def findValue(self, key):
        with open(FOODCSV, 'r') as f:
            readCSV = csv.DictReader(f, quotechar='"', fieldnames=FIELDNAMES)
            for row in readCSV:
                if row['Registry name'] == self.id:
                    return row[key]
            return None


    def generateRecipe(self):
        RECIPEDICT = settings.RECIPEDICT
        if self.id in RECIPEDICT:
            self.recipe = RECIPEDICT[self.id]
            return self.recipe
        else:
            self.weight = 1
            if self.isCooked():
                self.weight += 1
            return None


    def generateWeight(self):
        FOODDICT = settings.FOODDICT
        if self.weight > 0.0:
            return self.weight
        
        

        if self.recipe.foods != set():
            weight = 0
            for item in self.recipe.foods:
                try:
                    foodWeight = FOODDICT[item].weight
                    if foodWeight == 0.0:
                        return None
                    weight+=foodWeight
                except KeyError:
                    print(f'[-] {item} - KeyError')
        else:
            if self.isTofu() and self.isCooked():  # Used for cooked Tofu since no recipe.
                rawName = self.id.replace('cooked', 'raw')
                if FOODDICT[rawName].weight == 0.0:
                    return None
                weight = FOODDICT[rawName].weight + 1
            if self.isCooked():
                weight = 2.0
            else:
                weight = 1.0
            self.weight = weight

        return weight


    def genValues(self):
        if self.id in SPECIALFOODS:
            return (int(self.findValue('Hunger')), float(self.findValue('Saturation')))
        weight = self.weight
        if weight == 1:  # Morsels (no saturation)
            return (1, 0.0)
        if weight <= 3:  # Snacks (between 2-3 steps) (saturation half chunk)
            return (2, 0.125)  # Sat = 0.5
        if weight <= 5:  # Light Meal (between 4-5 steps) (saturation one less)
            return (5, .15)
        if weight <= 8:  # Meal (between 6-8 steps) (saturation equal)
            return (7, .2)
        if weight <= 11:  # Large Meal (Between 9-11 steps) (Saturation greater)
            return (9, .4)
        else:
            return (weight, .5)


    def isCooked(self):
        return 'Cooked' in self.findValue('Display name')


    def isRaw(self):
        return 'Raw' in self.findValue('Display name')


    def isTofu(self):
        return 'tofu' in self.id or 'ore:listAlltofu' in self.oredict


    def toCSV(self):
        return {
            'Registry name': self.id,
            'Weight': self.weight,
            'Product': self.product,
            'Hunger': self.hunger,
            'Saturation': self.saturation,
            'Display name': self.findValue('Display name'),
            'Ore Dict keys': self.oredict,
            'Mod name': self.findValue('Mod name'),
            'Item ID': self.findValue('Item ID'),
        }


    def toJson(self):
        hunger, saturation = self.genValues()
        return {
            'name': self.id,
            'hunger': hunger,
            'saturationModifier': saturation,
            'weight': self.weight,
        }


    def fromCSV(rowCSV):
        import re
        f = FoodItem(
            id = rowCSV['Registry name'],
            hunger = int(rowCSV['Hunger']),
            saturation = float(rowCSV['Saturation']),
            oredict = rowCSV['Ore Dict keys'],
            weight = float(rowCSV['Weight']),
            product = int(rowCSV['Product'])
        )
        if f.weight != 1.0:
            f.weight = 0.0
        return f

