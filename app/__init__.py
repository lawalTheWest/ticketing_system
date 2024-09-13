#!/usr/bin/env python3
# app/__init__.py
'''
    initialize flask app and also
    register blueprint from routes.py
'''
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .routes import routes
from config import Config

'''initialize my extensions'''
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'routes.Login'


def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    '''database configuration'''
    app.config.from_object(Config)
    
    ''' initializing the app with extesions'''
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    
    '''
        register Blueprint
    '''
    app.register_blueprint(routes)

    from .base_model import User, Ticket, Appointment
    
    @login_manager.user_loader
    def load_user(user_id):
        return user.query.get(int(user_id))
    
    return app