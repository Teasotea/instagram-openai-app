from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, redirect, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
import datetime
import sys

from . import db
from .utils.verification import send_verification_email
from .utils.verification  import confirm_token

auth = Blueprint("auth", __name__)

@auth.route("/login")
def login():
    return render_template("login.html")

@auth.route("/login", methods=["POST"])
def login_post():
    try:
        email = request.form["email"]
        password = request.form["password"]
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()
        print(f"{user = }")

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("auth.login"))

        if not user.email_verified:
            flash("Please verify your email and try again")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))


    except Exception as e:
        raise e

@auth.route("/signup")
def signup():
    return render_template("signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email address already exists")
            return redirect(url_for("auth.signup"))

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha256"),
            registered_on = datetime.datetime.now(),
            email_verified = False,
        )

        db.session.add(new_user)
        db.session.commit()

        send_verification_email(email)

        return redirect(url_for("auth.login"))

@auth.route('/verify/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_verified:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.email_verified = True
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.login'))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route("/profile", methods=["POST"])
@login_required
def add_info():
    instagram_key = request.form["ig_key"]
    instagram_username = request.form["ig_username"]

    if current_user.instagram_key != None:
         flash('You have added your Instagram API Key before.',  "warning")
         return redirect(url_for("main.profile"))

    current_user.instagram_key = instagram_key
    current_user.instagram_username = instagram_username
    db.session.commit()
    flash('Instagram API Key is added. Thanks!', 'success')
    
    return redirect(url_for("main.profile"))

@auth.route('/webhook', methods=['POST','GET'])
def webhook():
    print("Debug message here : 1", file=sys.stderr)

    if request.method == 'POST':
        print("POST", file=sys.stderr)
        print(request.json, file=sys.stderr)
        return 'success', 200
    elif request.method == 'GET':
        print(request.json, file=sys.stderr)
        challenge = request.args.get('hub.challenge')
        print(challenge, file=sys.stderr)
        if challenge == None:
            return '',200
        else:
            return challenge
    else:
        print("Debug message here : 2", file=sys.stderr)
        return '',200
