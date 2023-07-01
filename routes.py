from flask import render_template, request, Blueprint, url_for
from markupsafe import escape
import os
import numpy as np
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


routes = Blueprint(__name__, "routes")




@routes.route("/")
def home():

    img_list = os.listdir("static/dataset/pics")
    random_img_name = img_list[np.random.randint(0, len(img_list))]
    return render_template("index.html", img_name=random_img_name)



class
