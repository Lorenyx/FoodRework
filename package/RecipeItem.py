from dataclasses import dataclass, field
from . import settings


@dataclass
class RecipeItem:
    name: str
    recipe: list  # Contains duplicates
    foods: set = field(init=False)
    product: int = 1
    

    def generateFoods(self):
        self.foods = set()
        for item in self.recipe:
            if item in settings.FOODDICT:
                self.foods.add(item)
            elif item in settings.OREDICT:
                self.foods.add(settings.OREDICT[item][0])

    
        

    
