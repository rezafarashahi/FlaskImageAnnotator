from flask import render_template, request, Blueprint, url_for
from markupsafe import escape
import os


routes = Blueprint(__name__, "routes")




@routes.route("/")
def home():
    args = request.args
    return render_template("index.html")