import glob
import numpy
import json
import urllib.request
import csv
from hashlib import md5

import requests
import shutil


def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

odir = "data/images"

collection_url = "https://nakamura196.github.io/kunshujo-i/collection/kunshujo_curation.json"

response = urllib.request.urlopen(collection_url)
response_body = response.read().decode("utf-8")
collection = json.loads(response_body)

curations = collection["curations"]

for i in range(len(curations)):
    print(i)
    curation_url = curations[i]["@id"]

    response = urllib.request.urlopen(curation_url)
    response_body = response.read().decode("utf-8")
    curation = json.loads(response_body)

    selections = curation["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:
            thumbnail = member["thumbnail"]

            id = member["@id"]
            print(id)

            hash = md5(id.encode('utf-8')).hexdigest()

            thumbnail = thumbnail.replace("/,300/", "/,600/")

            download_img(thumbnail, odir+"/"+hash+".jpg")
