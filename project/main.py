from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/login')
def login():
    return render_template('login.html')