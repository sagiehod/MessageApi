from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth = Blueprint('auth', __name__)


@auth.route('/login/')
def login():
    #  log the user in
    username = request.args.get('username')
    password = request.args.get('password')
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return 'incorrect username or password'

    login_user(user)
    return 'Logged in successfully.'


@auth.route('/signup/')
def signup_post():
    # code to validate and add user to database goes here
    # get the username and password from url params
    username = request.args.get('username')
    password = request.args.get('password')
    # generate the hash
    password_hash = generate_password_hash(password, method='sha256')
    # add user to database
    user = User(username=username, password=password_hash)
    db.session.add(user)
    db.session.commit()  # commit the change
    return 'Successful signup'


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return 'Logged out successfully.'
