# str = 'recipes.addShaped("undergroundbiomes: siltstone_sandstone", < undergroundbiomes: sedimentary_sandstone: 3 > , [[ < undergroundbiomes:sedimentary_sand:3 > , < undergroundbiomes:sedimentary_sand:3 > ], [ < undergroundbiomes:sedimentary_sand:3 > , < undergroundbiomes:sedimentary_sand:3 > ]]);'
# import re
# words = re.findall('<(.*?)>', "".join(str.split()))
   
# print({'name': f'<{words[0]}>', 'mats': { f'<{i}>': words[1:].count(i) for i in words[1:] } })

set(['ore:cobblestone', 'ore:stickWood', 'ore:foodSalt', 'ore:foodSalt', 'ore:foodSalt', 'ore:materialPigskin', 'ore:foodHotsauce', 'minecraft:gunpowder', 'ore:foodGroundnutmeg', 'ore:foodMustard', 'ore:foodGarammasala', 'ore:foodGroundnutmeg', 'ore:foodSpiceleaf', 'minecraft:speckled_melon', 'ore:seedMustard', 'ore:foodGroundmutton', 'ore:seedMustard', 'ore:seedMustard', 'ore:foodGroundvenison', 'ore:seedMustard', 'ore:dyeGreen', 'ore:stickWood', 'ore:foodKetchup', 'harvestcraft:honey', 'ore:foodMustard', 'ore:foodSesameoil', 'ore:foodHotsauce', 'ore:flourEqualswheat', 'minecraft:redstone', 'minecraft:iron_ingot', 'ore:foodGroundnutmeg', 'ore:stickWood', 'harvestcraft:doughitem', 'ore:cropLychee', 'ore:foodKetchup', 'ore:foodKetchup', 'minecraft:iron_ingot', 'minecraft:gold_ingot', 'minecraft:redstone', 'minecraft:diamond', 'minecraft:coal', 'ore:foodSaladdressing', 'harvestcraft:potitem', 'ore:foodMustard', 'ore:foodHotsauce', 'minecraft:blaze_powder', 'ore:foodGroundnutmeg', 'minecraft:paper', 'ore:foodGarammasala', 'ore:foodCurrypowder', 'ore:foodKetchup', 'minecraft:gold_nugget', 'ore:foodSesameoil', 'ore:cropWheat', 'ore:materialPigskin', 'ore:cropPumpkin', 'ore:cropPumpkin', 'ore:cropPumpkin', 'ore:cropPumpkin', 'minecraft:pumpkin_seeds', 'ore:foodHotsauce', 'ore:foodYogurt', 'ore:listAllseed', 'ore:listAllseed', 'ore:foodKetchup', 'ore:foodKetchup', 'ore:foodMustard', 'ore:foodGroundnutmeg', 'ore:foodMustard', 'ore:foodMustard', 'harvestcraft:bakewareitem', 'minecraft:bone', 'ore:cropPumpkin', 'minecraft:double_plant', 'ore:foodSpiceleaf', 'ore:foodGroundnutmeg', 'ore:foodSweetandsoursauce', 'ore:foodKetchup', 'ore:cropPumpkin', 'ore:foodCurrypowder', 'ore:foodKetchup', 'minecraft:blaze_powder', 'ore:foodSalt', 'ore:stickWood', 'minecraft:redstone', 'ore:foodHotsauce', 'ore:foodSaladdressing', 'harvestcraft:potitem', 'minecraft:slime_ball', 'ore:listAllsalt', 'minecraft:nether_star', 'ore:cropPumpkin', 'ore:cropPumpkin', 'ore:foodGroundnutmeg', 'ore:listAllseed', 'ore:foodMustard', 'ore:stickWood', 'ore:foodKetchup'])


COOKINGTOOLS = [
    'animania:carving_knife',
    'ore:toolBakeware',
    'ore:toolMixingbowl',
    'ore:toolMortarandpestle',
    'ore:toolPot',
    'ore:toolSaucepan',
    'ore:toolCuttingboard',
    'ore:toolJuicer',
    'ore:toolSkillet',
    'minecraft:dye',
    'ore:foodOliveoil',
    'ore:foodVinegar',
    'ore:foodVanilla',
    'ore:foodGroundcinnamon',
    'ore:foodSoysauce',
    'ore:foodHoisinsauce',
    'ore:foodCornmeal',
    'ore:foodDough',
    'ore:foodMeringue',
    'ore:foodButter',
    'ore:foodBatter',
    'ore:foodFlour',
    'ore:foodPasta',
    'ore:foodNoodles',
    'ore:foodMayo',
    'ore:foodBlackpepper',
    'ore:foodCocoapowder',
    'ore:dustSalt',
    'ore:itemSalt',
    'ore:foodFivespice',
    'ore:foodGroundbeef',
    'ore:foodGroundpork',
    'minecraft:snowball',  # Smoothies
    'forge:bucketfilled',
    'minecraft:milk_bucket',
    'ore:listAllwater',
    'ore:foodBubblywater',
    'minecraft:glass_bottle',
    'minecraft:bowl',
    'betternether:stalagnate_bowl',
    'minecraft:nether_wart',
    'biomesoplenty:mushroom',
    'rats:plague_essence',
    'minecraft:reeds',
    'bountifulbaubles:trinketshulkerheart',  # Sandwich Horror
    'ore:flower',
    'minecraft:cactus',
    'minecraft:flint',
    'ore:foodSesameoil', 'ore:foodGarammasala', 'minecraft:redstone', 'ore:cropPumpkin', 'ore:cobblestone', 'ore:listAllsalt', 'ore:cropLychee', 'ore:cropWheat', 'minecraft:speckled_melon', 'ore:foodHotsauce', 'ore:stickWood', 'ore:foodSweetandsoursauce', 'ore:dyeGreen', 'minecraft:bone', 'minecraft:slime_ball', 'ore:foodGroundvenison', 'minecraft:blaze_powder', 'ore:flourEqualswheat', 'harvestcraft:doughitem', 'minecraft:coal', 'harvestcraft:potitem', 'minecraft:iron_ingot',
    'minecraft:diamond', 'ore:foodGroundnutmeg', 'ore:listAllseed', 'ore:foodMustard', 'minecraft:paper', 'ore:foodSalt', 'ore:foodYogurt', 'harvestcraft:bakewareitem', 'minecraft:double_plant', 'minecraft:gunpowder', 'ore:foodSaladdressing', 'ore:seedMustard', 'ore:foodCurrypowder', 'minecraft:nether_star', 'ore:foodSpiceleaf', 'minecraft:gold_ingot', 'minecraft:gold_nugget', 'ore:foodKetchup', 'ore:materialPigskin', 'harvestcraft:honey', 'ore:foodGroundmutton', 'minecraft:pumpkin_seeds'
    # Miner Stew
]

import json

dict = json.load(open('tools.json', 'r'))

print('weight' in dict)