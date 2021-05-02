from requests import get
import re

from dataclasses import dataclass, field
from collections import namedtuple
from typing import NamedTuple, List

from .config import MORSEL_PATTERN, URL


@dataclass
class ZenScriptParser:
    zs_file = field(init=False)
    morsels: List[NamedTuple] = field(init=False, default_factory=list)
    recipes: List[str] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.zs_file = get()

    
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
                
    
    

