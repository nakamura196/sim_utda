import glob
import numpy
import json
import urllib.request
import csv
from hashlib import md5
from helper import *
import requests
import shutil

files = glob.glob("data/image_vectors/*.npy")

features = []

for file in files:
    a = numpy.load(file)
    features.append(a)

numpy.save('data/features.npy', features)

with open('data/features_list.json', 'w') as outfile:
    json.dump(files, outfile, ensure_ascii=False,
              sort_keys=True, separators=(',', ': '))

