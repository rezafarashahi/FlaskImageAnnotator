from flask import render_template, request, Blueprint, url_for
from markupsafe import escape
import os
import numpy as np


routes = Blueprint(__name__, "routes")




@routes.route("/")
def home():

    img_list = os.listdir("dataset/pics")
    random_img_name = img_list[np.random.randint(0, len(img_list))]
    return render_template("index.html", img_name=random_img_name)