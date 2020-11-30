from package import settings

if __name__ == '__main__':
    settings.init()
    fd = settings.FOODDICT
    food = fd['harvestcraft:zucchinifriesitem']

    print(food.oredict)
    print(fd['animania:friesian_cheese_wedge'])
    print(fd['harvestcraft:toastitem'])
    print(fd['betterwithmods:raw_egg'])
    print(fd['harvestcraft:zucchiniitem'])
    # harvestcraft:cookedtofurkeyitem
    # harvestcraft:rawtofurkeyitem
