from os import stat
import re

from dataclasses import dataclass, field
from io import TextIOWrapper
from collections import namedtuple

from typing import NamedTuple, List

from .config import MORSEL_PATTERN


def zstrip(__src: str):
    "Removes all newline and tab characters"
    return __src.replace('\n', '').replace('\t', '')


@dataclass
class ZenScriptParser:
    __file_name: str = 'ex_sartagine.zs'
    zs_file: TextIOWrapper = field(init=False)
    morsels: List[NamedTuple] = field(init=False, default_factory=list)
    recipes: List[str] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.zs_file = open(self.__file_name)

    
    def parse_line(self, line: str):
        
        if line.startswith('//'):
            line = next(self.zs_file)
        elif line.startswith('/*'):
            while not next(self.zs_file).startswith('*/'):
                continue
            line = next(self.zs_file)
        if zstrip(line):
            print(repr(line) + 'has passed')
        print(repr(zstrip(line)))


    def start(self):
        for x in range(75):
            self.parse_line(next(self.zs_file))
                
    
    

