from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect, abort
) 
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user
from .forms import LoginForm
from settings.models import User
from settings import botDB
from . import isDiscordBotReady

#create blueprint
bp = Blueprint('auth', __name__)

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    status = isDiscordBotReady()
    if status is not True:
        return status
    form = LoginForm()
    error=None
    if(form.validate_on_submit()):
        user_name = form.username.data
        password = form.password.data
        UserResult = User.get(user_name)
        
        # Check if there is user with that name
        if (UserResult is None) or not check_password_hash(UserResult.password, password):
            error='Incorrect user name or password'

        if error is None:
            #sign in and set the login user
            login_user(UserResult)
            next = request.args.get('next')

            return redirect(next or url_for('adminPanel.index'))
        else:
            flash(error)

        #it comes here when it is a get method
    return render_template('login.html', form=form)
'''
@bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('Register form submitted')
        #get username, password and email from the form
        uname = form.username.data
        pwd = form.password.data
        # don't store the password - create password hash
        pwd_hash = generate_password_hash(pwd)
        #create a new user model object
        new_user = User(username=uname, password_hash=pwd_hash)
        db.session.add(new_user)
        db.session.commit()
        #commit to the database and redirect to HTML page
        return redirect(url_for('auth.register'))
    
    return render_template('login.html', pageTitle="Compubay - Register", form=form, heading='Register')
'''
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))