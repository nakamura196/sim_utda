from flask import Flask, render_template, request, jsonify  # 追加
from helper import *
from random import *
import urllib.request
import json
import numpy
from scipy import spatial
import os
from flask_cors import CORS
from annoy import AnnoyIndex
from nltk import ngrams
import random
import glob
import os
import codecs
import random
import numpy as np
import collections
# ソースコード
import copy

app = Flask(__name__,
            static_folder="./dist/static",
            template_folder="./dist")
CORS(app)

app.config['JSON_AS_ASCII'] = False  # 日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False  # ソートをそのまま

MODEL_PATH = 'classify_image_graph_def.pb'

print("... Loading features.npy")

path = "features.npy"
features2 = numpy.load(path)

######

'''

# data structures
file_index_to_file_name = {}
file_index_to_file_vector = {}

# config
dims = 2048
n_nearest_neighbors = 60
trees = 10000
infiles = glob.glob('image_vectors/*.npy')

# build ann index
t = AnnoyIndex(dims)
for file_index, i in enumerate(infiles):
    file_vector = np.load(i)
    file_name = os.path.basename(i).split('.')[0]
    file_index_to_file_name[file_index] = file_name
    file_index_to_file_vector[file_index] = file_vector
    t.add_item(file_index, file_vector)
t.build(trees)

'''

######

print("... End of Loading features.npy")

print("... Loading data.json")


with open('data.json') as f:
    files = json.load(f)

metadata = {}
for id in files:
    metadata_array = files[id]["metadata"]
    for obj in metadata_array:
        label = obj["label"]
        value = obj["value"]

        if label not in metadata:
            metadata[label] = {}

        if value not in metadata[label]:
            metadata[label][value] = []

        if id not in metadata[label][value]:
            metadata[label][value].append(id)

metadata_summary = {}

for field in metadata:
    obj = metadata[field]

    metadata_summary[field] = {}

    for label in obj:
        metadata_summary[field][label] = len(obj[label])

    sorted_x = sorted(
        metadata_summary[field].items(), key=lambda kv: kv[1], reverse=True)
    metadata_summary[field] = collections.OrderedDict(sorted_x)

print("... End of Loading data.json")

@app.route('/')
def index():
    return render_template("index.html")


'''

@app.route('/api/search2')
def api_search2():

    index = request.args.get('index', default=-1, type=int)
    url = request.args.get('url', default=None, type=str)
    CANDIDATES = request.args.get('rows', default=40, type=int)

    CANDIDATES -= 1

    if index != -1:

        query_feat = features2[index]

    elif url != None:

        query_img = "/tmp/tmp.jpg"
        urllib.request.urlretrieve(url, "{0}".format(query_img))

        with tf.gfile.FastGFile(MODEL_PATH, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        print("... End of FastGFile")

        with tf.Session() as sess:
            pool3 = sess.graph.get_tensor_by_name('pool_3:0')

            image_data = tf.gfile.FastGFile(query_img, 'rb').read()
            pool3_features = sess.run(
                pool3, {'DecodeJpeg/contents:0': image_data})
            query_feat = np.squeeze(pool3_features)

        print("... End of Session")

    else:
        return jsonify([])

    master_vector = query_feat

    data = []

    nearest_neighbors = t.get_nns_by_vector(master_vector, n_nearest_neighbors)

    for j in nearest_neighbors:
        neighbor_file_name = file_index_to_file_name[j]
        neighbor_file_vector = file_index_to_file_vector[j]

        similarity = 1 - \
            spatial.distance.cosine(master_vector, neighbor_file_vector)
        rounded_similarity = int((similarity * 10000)) / 10000.0

        # obj = files[str(index)]
        obj = files[neighbor_file_name]
        # obj["filename"] = neighbor_file_name
        # obj["path"] = files[index]
        obj["score"] = rounded_similarity
        data.append(obj)

    return jsonify(data)

'''


@app.route('/api/search')
def api_search():

    index = request.args.get('index', default=-1, type=int)
    url = request.args.get('url', default=None, type=str)
    CANDIDATES = request.args.get('rows', default=40, type=int)

    CANDIDATES -= 1

    if index != -1:

        query_feat = features2[index]

    elif url != None:

        query_img = "/tmp/tmp.jpg"
        urllib.request.urlretrieve(url, "{0}".format(query_img))

        with tf.gfile.FastGFile(MODEL_PATH, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        print("... End of FastGFile")

        with tf.Session() as sess:
            pool3 = sess.graph.get_tensor_by_name('pool_3:0')

            image_data = tf.gfile.FastGFile(query_img, 'rb').read()
            pool3_features = sess.run(
                pool3, {'DecodeJpeg/contents:0': image_data})
            query_feat = np.squeeze(pool3_features)

        print("... End of Session")

    else:
        return jsonify([])

    sims = [(k, round(1 - spatial.distance.cosine(query_feat, v), 3))
            for k, v in enumerate(features2)]

    data = []

    arr = sorted(sims, key=operator.itemgetter(1),
                 reverse=True)[:CANDIDATES + 1]
    for e in arr:
        index = e[0]

        # temp
        if str(index) not in files:
            continue

        obj = copy.copy(files[str(index)])
        # obj["path"] = files[index]
        obj["score"] = e[1]
        data.append(obj)

    return jsonify(data)

@app.route('/api/msearch')
def api_msearch():

    where_metadata_label = request.args.get(
         'where_metadata_label', default=None, type=str)
    where_metadata_value = request.args.get(
        'where_metadata_value', default=None, type=str)
    rows = request.args.get('rows', default=40, type=int)

    metadata_arr = metadata[where_metadata_label][where_metadata_value]

    if rows > len(metadata_arr):
        rows = len(metadata_arr)

    indexes = random.sample(metadata_arr, rows)

    data = []

    for index in indexes:
        obj = files[str(index)]
        data.append(obj)

    return jsonify(data)

@app.route('/api/random')
def api_random():

    rows = request.args.get('rows', default=40, type=int)

    data = []

    import random
    indexes = random.sample(files.keys(), rows)

    for index in indexes:
        obj = files[str(index)]
        data.append(obj)

    return jsonify(data)


@app.route('/api/metadata')
def api_metadata():


    return jsonify(metadata_summary)


# おまじない
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
