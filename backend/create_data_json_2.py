import glob
import numpy
import json
import urllib.request
import csv
from hashlib import md5
from helper import *
import requests
import shutil

with open('data/features_list.json') as f:
    df = json.load(f)

data = {}

for i in range(len(df)):
    id = df[i].split("/")[-1].split(".")[0]

    obj = {
        "id": "https://example.org/"+id,
        "index": i,
        "label": id,
        "thumbnail": "http://localhost:8888/flaskvue4ut/backend/data/images/"+id+".jpg"
    }

    data[id] = obj

with open('data/data.json', 'w') as outfile:
    json.dump(data, outfile, ensure_ascii=False,
              sort_keys=True, separators=(',', ': '))
