from werkzeug.utils import redirect
from app import app, mongo
from app.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, redirect, flash, session
import sys

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html', title='Home')
    
@app.route('/about')
def about():
    usuarios = mongo.db.users.find()
    return render_template('about.html', title='About', informacion=usuarios)
    
@app.route('/account')
def account():
    info = None
    if 'username' in session:
        info = {'username': session['username'], 'email': session['email']}
    return render_template('account.html', title='Account', info=info)
   
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"username": form.username.data})
        print(form)
        if user:
            flash(f'An account with the username {form.username.data} already exists', category='danger')
            return render_template('signup.html', title='SignUp', form=form)
        else:
            if mongo.db.users.insert({"username": form.username.data, "password": form.password.data, "email": form.email.data}):
                flash(f'Account created succesfully for {form.username.data}', category='success')
                return redirect(url_for('login'))
            else:
                flash(f'There was an error creating the user, try again', category='danger')
                return render_template('signup.html', title='SignUp', form=form)
    return render_template('signup.html', title='SignUp', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"username": form.username.data})
        if user:
            print('Existe un usuario con ese nombre', file=sys.stdout)
            if user['password'] == form.password.data:
                session['username'] = form.username.data
                session['email'] = user['email']
                flash(f'Login successful for the user: {form.username.data}', category='success')
                return redirect(url_for('account'))
            else:
                flash(f'The password doesn\'t match', category='danger')
                return render_template('login.html', title='Login', form=form)
        else:
            print('Error, no existe un usuario con ese nombre', file=sys.stderr)
            flash(f'Login unsuccessful for the user: {form.username.data}', category='danger')
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('home.html', title='Home')