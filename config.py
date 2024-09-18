# config.py
'''
    configuration management
'''
import os

database = os.path.abspath(os.path.dirname(__file__))

class Config():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    '''
        Secret key for session management
        Using python to generate a more secure key:
            import os
            print(os.urandom(24).hex())
    '''
    SECRET_KEY = os.environ.get('SECRET_KEY') or '47ce33347f06535cba7b29686ae302ca4d62325e86e287cf'
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USERNAME = '@gmail.com'
    # MAIL_PASSWORD = 'your-email-password'
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False