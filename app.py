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


app = Flask(__name__)
app.register_blueprint(routes, url_prefix="/")
app.config['SECRET_KEY'] = "This is a secret key"

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

@app.route('/get_labled_data', methods=["POST"])
@login_required
def create_entry():

    req = request.get_json()
    print(req)

    res = make_response(jsonify({"message": "JSON received"}), 200)

    return res


@app.route('/')
def home():
    return redirect(url_for("login"))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    img_list = os.listdir("static/dataset2/images")
    random_img_name = img_list[np.random.randint(0, len(img_list))]
    return render_template("dashboard.html", img_name=random_img_name)

@app.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    img_list = os.listdir("static/dataset2/images")
    random_img_name = img_list[np.random.randint(0, len(img_list))]
    # random_img_name = img_list[3]
    a = pd.read_csv("static/dataset2/labels/{}{}".format(random_img_name[:-3], 'txt'), sep=" ",
                    header=None)
    # return render_template("dashboard.html", img_name=random_img_name, a=a)
    print(a)
    return render_template("test.html", a=a.values.tolist(), img=random_img_name)


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

    app.run(debug=True, host='0.0.0.0')