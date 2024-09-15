#!/usr/bin/env python3
# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from wtforms import StringField, PasswordField, SubmitField
from app import db
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from .base_model import User
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt

bycrypt = Bcrypt()
routes = Blueprint('routes', __name__)

# Forms
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4,max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=4, max=80)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=4,max=80)])
    phone_number = StringField('Phone Number', validators=[InputRequired(), Length(min=8, max=20)])
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
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            try:
                if user.check_password(form.password.data):
                    login_user(user)
                    flash('Logged in Successfulyy', 'success')
                    return redirect(url_for('routes.Dashboard'))
                else:
                    flash('Invalid Email or Password', 'danger')
            except ValueError:
                flash("There was an issue with your account \n please")
                return redirect(url_for('routes.reset_password'))
    else:
        # print(form.errors)
        flash('Invalid Email or Password!', 'danger')
    return render_template('login.html', form=form)

@routes.route('/register', methods=['Get', 'Post'])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        # hashed_password = bycrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        phone_number=form.phone_number.data)
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


@routes.route('/reset_password')
def Reset_password():
    return render_template('resetPassword.html')