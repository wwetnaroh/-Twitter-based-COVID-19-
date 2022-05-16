import csv
import json
import os
import place

path = './dataset'
files = os.listdir(path)

for file in files:
    date = file.split('.')[0]
    # print(date)
    data = {
        "type":"FeatureCollection"
    }
    feature = []
    with open('./dataset/' + file, 'r') as f:
        cnt = 0
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            # print(row)
            state = row[0]
            if state == "American Samoa" or state == "Diamond Princess" or state == "Grand Princess" or state == "Guam" or state == "Northern Mariana Islands" or state == "Virgin Islands" or state == 'Recovered':
                continue
            cnt += 1
            datarow = {
                "type": "Feature",
                "id": str(cnt),
                "properties": {
                    "name": state,
                    'confirmed': int(row[5]),
                    'death': int(row[6])
                },
                "geometry": place.coordinate[state]
            }
            # print(datarow)
            feature.append(datarow)
    data["features"] = feature
    with open('./jsonfile/' + date + '.json', 'w') as jsf:
        json.dump(data, jsf)

