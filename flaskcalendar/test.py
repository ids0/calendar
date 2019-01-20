import json
import os
path = os.path.join(os.pardir,'config.json')


with open(path) as config_file:
    config = json.load(config_file)
    print(config)
input()