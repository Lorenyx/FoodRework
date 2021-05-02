from collections import namedtuple

URL = 'https://raw.githubusercontent.com/Rebirth-of-the-Night/Rebirth-Of-The-Night/master/scripts/ex_sartagine.zs'
MORSEL_PATTERN = r'va[lr] \w+ = <\w+:\w+>;'


Morsel = namedtuple('Morsel', ['name', 'id'])