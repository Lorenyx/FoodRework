with open('recipes.dat', 'r') as f:
    count = 0
    for row in f:
        if count == 7:
            break
        ls = row.split(', ', maxsplit=2)
        
        if len(ls) > 1 and '*' in ls[1]:
            print(ls[1][str.index('*')+2:])

print('harvestcraft:breadedporkchopitem' == '"harvestcraft:breadedporkchopitem"')
