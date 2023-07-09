from flask import render_template, request, Blueprint, url_for, flash, redirect
from markupsafe import escape
import os
import numpy as np
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

routes = Blueprint(__name__, "routes")




# @routes.route("/")
# def home():
#
#     return render_template("login.html")




class NamerForm(FlaskForm):
    name = StringField("What's your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")



