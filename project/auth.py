from flask_login import login_user, login_required, logout_user
from flask import Blueprint,  render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
from .models import User
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    try:
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        with sql.connect("db.sqlite") as con:
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=remember)

            if not user or not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
    except:
        con.rollback()
        msg = "error in insert operation"

    finally:
        return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    try:

        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        with sql.connect("db.sqlite") as con:
            #cur = con.cursor()

            user = User.query.filter_by(email=email).first() 

            if user:
                flash('Email address already exists')
                return redirect(url_for('auth.signup'))

            new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

            con.add(new_user)
            con.commit()
            
    except:

        con.rollback()
        msg = "error in insert operation"

    finally:
        return  redirect(url_for('auth.login'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

