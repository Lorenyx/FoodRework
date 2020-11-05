# str = 'recipes.addShaped("undergroundbiomes: siltstone_sandstone", < undergroundbiomes: sedimentary_sandstone: 3 > , [[ < undergroundbiomes:sedimentary_sand:3 > , < undergroundbiomes:sedimentary_sand:3 > ], [ < undergroundbiomes:sedimentary_sand:3 > , < undergroundbiomes:sedimentary_sand:3 > ]]);'
# import re
# words = re.findall('<(.*?)>', "".join(str.split()))
   
# print({'name': f'<{words[0]}>', 'mats': { f'<{i}>': words[1:].count(i) for i in words[1:] } })

x = '\w'

print( x.isspace())
