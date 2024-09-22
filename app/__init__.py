# app/__init__.py
'''
    initialize flask app and also
    register blueprint from routes.py
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
from flask import Flask, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

'''initialize my extensions'''
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
config = Config()

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
    bcrypt.init_app(app)
    
    '''
        register Blueprint
    '''
    from .routes import routes
    app.register_blueprint(routes)
    login_manager.init_app(app)
    login_manager.login_view = 'routes.Login'
    
    from .base_model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app