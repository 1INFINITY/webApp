from flask import Blueprint, flash
from flask_login import login_user
from .models import User
from .__init__ import db
from flask import Flask, render_template, url_for, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        flash('Start')
        name = request.form['floatingInput']
        password = request.form['floatingPassword']
        password_repeat = request.form['floatingPasswordRepeat']
        if not (name or password or password_repeat):
            flash('Please fill all fields!')
        elif password != password_repeat:
            flash('Passwords are different')

        user = User.query.filter_by(name=name).first()  # if this returns a user, then the email already exists in database

        if user:
            flash('Email address already exists')  # if a user is found, we want to redirect back to signup page so user can try again
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    else:
        return render_template("sign_up.html")

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        name = request.form['floatingInput']
        password = request.form['floatingPassword']
        if name and password:
            user = User.query.filter_by(name=name).first()

            if check_password_hash(user.password, password):
                login_user(user)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("sign_in.html")


@auth.route('/logout')
def logout():
    return 'Logout'
