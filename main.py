import requests

resp = requests.get('https://raw.githubusercontent.com/Rebirth-of-the-Night/Rebirth-Of-The-Night/master/scripts/ex_sartagine.zs')

for line in resp.iter_lines(delimiter=b';\n'):
    print(line)




