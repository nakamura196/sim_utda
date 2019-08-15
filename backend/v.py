from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import requests
import numpy as np

import os
import json
import glob
import re

import time

model = VGG16(include_top=True, weights='imagenet',
              input_tensor=None, input_shape=None)


#画像をダンロードするための関数
def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)


fj = open('ILSVRC2012.json', 'r', encoding='UTF-8')
tojp = json.load(fj)
fj.close()


if __name__ == '__main__':

    files = glob.glob("data/images/*.jpg")

    for i in range(len(files)):
        file = files[i]

        if i % 10 == 0:
            print(str(i+1)+"/"+str(len(files)))

        file = files[i]

        opath = file.replace("/images/", "/tags/")+".json"

        if not os.path.exists(opath):

            try:

                img = image.load_img(file, target_size=(224, 224))

                # 読み込んだPIL形式の画像をarrayに変換
                ary = image.img_to_array(img)

                #サンプル数の次元を1つ増やし四次元テンソルに
                ary = np.expand_dims(ary, axis=0)

                #上位5を出力
                preds = model.predict(preprocess_input(ary))
                results = decode_predictions(preds, top=5)[0]

                arr = []

                for result in results:
                    replaced_str = re.sub('\'', '', result[1], count=0)
                    arr.append({
                        "label": tojp[replaced_str],
                        "score": float(result[2])
                    })

                fw = open(opath, 'w')

                json.dump(arr, fw, ensure_ascii=False, indent=4,
                          sort_keys=True, separators=(',', ': '))

            except:
                time.sleep(1)
                print(file)
