#!/usr/bin/env python3
# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from wtforms import StringField, PasswordField, SubmitField
# from app import db
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from .base_model import User


routes = Blueprint('routes', __name__)

# Forms
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4,max=80)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password')])
    confirm_password = PasswordField('Confirm PAssword', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username not Available!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email not Available!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

@routes.route('/')
def Home():
    '''Defines the home function'''
    return render_template("home.html")

@routes.route('/about')
def About():
    '''defines the about function'''
    return render_template('about.html')

@routes.route('/login', methods=['Get', 'Post'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in SUccessfulyy', 'success')
            return redirect(url_for('routes.Dashboard'))
        else:
            flash('Invalid Email or Password')
    return render_template('login.html', form=form)

@routes.route('/register', methods=['Get', 'Post'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        first_name='firstName',
                        last_name='lastName',
                        phone_number='00000000000')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Created Successfully! You can now Log in.', 'success')
        return redirect(url_for('routes.Login'))
    return render_template('register.html', form=form)

@routes.route('/logout')
@login_required
def Logout():
    logout_user()
    flash('Logged out Successfully!', 'info')
    return redirect(url_for('routes.Home'))

@routes.route('/dashboard')
@login_required
def Dashboard():
    return render_template('dashboard.html', name=current_user.username)