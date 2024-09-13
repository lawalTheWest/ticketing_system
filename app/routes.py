#!/usr/bin/env python3
# app/routes.py

from flask import Blueprint, render_template
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm

routes = Blueprint('routes', __name__)

@routes.route('/')
def Home():
    '''Defines the home function'''
    return render_template("home.html")

@routes.route('/about')
def About():
    '''defines the about function'''
    return render_template('about.html')

@routes.route('/login')
def Login():
    return render_template('login.html')

@routes.route('/register')
def Register():
    return render_template('register.html')