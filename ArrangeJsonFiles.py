import os
import numpy as np
import json
import random

dir = 'static/dataset/images'
a = os.listdir(dir)
random.shuffle(a)

Sure = False
if Sure:

    for i in range(31):


        img_info = {
            "unlabeled": a[i*122:(i+1)*122-1],
            "labeled": []
        }
        with open(os.path.join('static/dataset/json/', 'img_ds{}.json'.format(i)), 'w') as jfile:

            json.dump(img_info, jfile)

        if i==30:
            img_info = {
                "unlabeled": a[i * 122:len(a)],
                "labeled": []
            }
            with open(os.path.join('static/dataset/json/', 'img_ds{}.json'.format(i)), 'w') as jfile:
                json.dump(img_info, jfile)
