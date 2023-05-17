from flask import Blueprint, flash, Flask, render_template, url_for, request, redirect
from flask_login import login_user, logout_user, login_required
from application.models import User
from application import db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form['floatingInput']
        password = request.form['floatingPassword']
        password_repeat = request.form['floatingPasswordRepeat']
        if not (name and password and password_repeat):
            flash('Please fill all fields!')
        elif password != password_repeat:
            flash('Passwords are different')
        else:
            # if this returns a user, then the email already exists in database
            user = User.query.filter_by(name=name).first()

            if user:
                # if a user is found, we want to redirect back to signup page so user can try again
                flash('This username is already exists')
                return redirect(url_for('auth.register'))

            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(name=name, password=generate_password_hash(password, method='sha256'))

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('auth.login'))
    return render_template("sign_up.html")


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        name = request.form['floatingInput']
        password = request.form['floatingPassword']
        remember = True if request.form.get('rememberInput') else False

        if name and password and name != '' and password != '':
            user = User.query.filter_by(name=name).first()
            if user and check_password_hash(user.password, password):
                login_user(user, remember=remember)
                return redirect(url_for('main.hello'))
            else:
                flash('Name or password is incorrect')
        else:
            flash('Please fill all fields!')
    return render_template("sign_in.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
