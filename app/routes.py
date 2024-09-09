#!/usr/bin/env python3
from flask import Blueprint, render_template

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return "hello world!"

