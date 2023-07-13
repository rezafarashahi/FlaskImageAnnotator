from flask import Flask, render_template, flash, Blueprint, url_for, request, redirect, jsonify, make_response
from routes import routes
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
import json
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import os
import pandas as pd
import json
import shutil

with open("config.json", "rb") as conf:
    config = json.load(conf)


app = Flask(__name__)
app.register_blueprint(routes, url_prefix="/")
app.config['SECRET_KEY'] = config['SECRET_KEY']

#Add Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#Initialize the database

db = SQLAlchemy(app)


# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Create a model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())

    #PASSWORD HASHING
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
            else:
                flash("Wrong username/password.")
        flash("Wrong username/password.")
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('login'))

@app.route('/get_labeled_data', methods=["POST"])
@login_required
def create_entry():

    req = request.get_json()
    ar = []
    for el in req['label_data']:
        ar.append([el[0]]+el[1])
    try:
        if ar:
            np.savetxt('static/dataset/labels/{}.txt'.format(req["img_name"][:-4]),
                       np.array(ar),
                       delimiter=' ',
                       fmt=['%d', '%.5f', '%.5f', '%.5f', '%.5f'])
            if 'img_ds{}.json'.format(req["rand_no"]) in os.listdir("static/dataset/json"):
                with open('static/dataset/json/img_ds{}.json'.format(req["rand_no"]), 'r') as r_f:
                    x = json.load(r_f)
            else:
                with open('static/dataset/json/img_ds{}_cp.json'.format(req["rand_no"]), 'r') as r_f:
                    x = json.load(r_f)

            x["labeled"].append([req["img_name"], ar])
            x["unlabeled"].remove(req["img_name"])

            with open('static/dataset/json/img_ds{}.json'.format(req["rand_no"]), 'w') as w_f:

                json.dump(x, w_f)

            res = make_response(jsonify({"message": "JSON received"}), 200)
            print(req["img_name"])
            print(req["rand_no"])

            return res
        else:
            return make_response(jsonify({"message": "JSON received"}), 202)
    except:

        return make_response(jsonify({"message": "JSON received"}), 202)


@app.route('/')
def home():
    return redirect(url_for("login"))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    for i in range(2):

        rand_no = np.random.randint(0, len(os.listdir("static/dataset/json")))
        with open('static/dataset/json/img_ds{}.json'.format(rand_no), 'r') as img:
            ds_list = json.load(img)
        if ds_list['unlabeled']:
            random_img_name = ds_list['unlabeled'][np.random.randint(0, len(ds_list['unlabeled']))]
            print(rand_no)
            print(random_img_name)
            break
        else:
            os.rename('static/dataset/json/img_ds{}.json'.format(rand_no),
                        'static/dataset/json/img_ds{}_cp.json'.format(rand_no))

    return render_template("dashboard.html", img_name=random_img_name, rand_no=rand_no)

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():

    img_list = os.listdir("static\dataset\labels")

    if img_list:
        random_img_name = img_list[np.random.randint(0, len(img_list))]
        random_img_name = "{}.jpg".format(random_img_name[:-4])
        # random_img_name = img_list[3]
        a = pd.read_csv("static/dataset/labels/{}{}".format(random_img_name[:-3], 'txt'), sep=" ",
                        header=None)
        # return render_template("dashboard.html", img_name=random_img_name, a=a)
        print(a)
        return render_template("test.html", a=a.values.tolist(), img=random_img_name)
    else:
        return redirect(url_for("dashboard"))


@app.route('/test2', methods=['GET', 'POST'])
@login_required
def test2():
    return render_template("test2.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

if __name__ == '__main__':

    app.run(debug=True)