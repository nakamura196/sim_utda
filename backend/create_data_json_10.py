import json
from SPARQLWrapper import SPARQLWrapper
import hashlib

flg = True

page = 0

map = {}

while (flg):

    print(page)

    sparql = SPARQLWrapper(endpoint='https://sparql.dl.itc.u-tokyo.ac.jp', returnFormat='json')
    sparql.setQuery("""
      SELECT DISTINCT ?url ?label ?provider_label ?thumb WHERE {
      ?s <http://purl.org/dc/terms/title> ?label .
      ?s <http://purl.org/dc/terms/relation> ?url. 
      ?s <http://ndl.go.jp/dcndl/terms/digitizedPublisher> ?provider_label . filter(LANG(?provider_label) = 'ja')
      ?s <http://xmlns.com/foaf/0.1/thumbnail> ?thumb . 
    } limit 10000 offset """ + str(10000 * page) + """
    """)

    results = sparql.query().convert()

    if len(results["results"]["bindings"]) == 0:
        flg = False

    page += 1

    for obj in results["results"]["bindings"]:
        url = obj["url"]["value"]
        label = obj["label"]["value"]
        attribution = obj["provider_label"]["value"]
        thumb = obj["thumb"]["value"]
        id = url.split("/")[-1]

        map[id] = {
            "thumbnail" : thumb,
            "id" : url,
            "label" : label,
            "metadata" : [
                {
                    "label" : "部局",
                    "value" : attribution
                }
            ]
        }

fw2 = open("data/data_0.json", 'w')
json.dump(map, fw2, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
