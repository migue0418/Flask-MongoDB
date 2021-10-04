from werkzeug.utils import redirect
from app import app, mongo
from app.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, redirect, flash

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
    return render_template('account.html', title='Account')
   
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created succesfully for {form.username.data}', category='success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='SignUp', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'migue' and form.password.data == '123456':
            flash(f'Login successful for {form.username.data}', category='success')
            return redirect(url_for('account'))
        else:
            flash(f'Login unsuccessful for {form.username.data}', category='danger')
            return redirect(url_for('homepage'))
    return render_template('login.html', title='Login', form=form)