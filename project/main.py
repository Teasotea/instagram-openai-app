from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, email = current_user.email)

@main.route('/signup')
def signup():
    return render_template('signup.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/logout')
def logout():
    return render_template('logout.html')

