#!/usr/bin/env python3
from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    '''Defines the home function'''
    return render_template("home.html")

@routes.route('/about')
def About():
    '''defines the about function'''
    return render_template('about.html')

# @routes.route('/')