from requests import get
import re
from config import URL

MORSELS = []

def main():
    zs_file = get(URL)
    re.sub()
    for line in zs_file.iter_lines(delimiter=b';\n'):
        
        print(str(line).replace())

if __name__ == '__main__':
    # main()
    tmp = 'i am   some\t lone\n wodds'
    out = re.sub('\s+', '', tmp)
    print(out)