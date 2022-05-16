import json
import os
from datetime import timedelta, datetime


path = './jsonfile'
files = os.listdir(path)

for file in files:
    date = file.split('.')[0]
    yesterday = date
    with open("./jsonfile/" + file,'r') as f:
        load_dict = json.load(f)
        print(load_dict)
        features = load_dict['features']
        for feature in features:
            state = feature['properties']['name']
            confirmed = feature['properties']['confirmed']

    break

