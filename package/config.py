from collections import namedtuple

MORSEL_PATTERN = r'va[lr] \w+ = <\w+:\w+>;'


Morsel = namedtuple('Morsel', ['name', 'id'])