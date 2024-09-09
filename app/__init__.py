#!/usr/bin/env python3
'''
    initialize flask app and also
    register blueprint from routes.py
'''
from flask import Flask
from .routes import routes

def create_app():
    app = Flask(__name__)

    '''
        register Blueprint
    '''
    app.register_blueprint(routes)
    # app.register_blueprint()

    return app