import csv
import json
import os

path = './csv'
files = os.listdir(path)

for file in files:
  # print(path + '/' + file)
  with open(file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    with open(path + '/' + file) as f:
      f_csv = csv.reader(f)
      for row in f_csv:
        row = row[0]
        # print(row)
        writer.writerow([row])

      