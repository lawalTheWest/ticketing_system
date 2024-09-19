# base_model.py
'''
    Database models:
        user, ticket, appointment
'''

from . import db, bcrypt
from flask_login import UserMixin
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    '''User class'''
    # User id - this is a unique primary key, autoincrement.
    id = db.Column(db.Integer,
                   primary_key=True)
    
    # username - unique and not null
    username = db.Column(db.String(80),
                         unique=True,
                         nullable=False)
    
    # user email - unique, not null
    email = db.Column(db.String(120),
                      unique=True,
                      nullable=False)
    
    # user password - not unique and not null
    password_hash = db.Column(db.String(255),
                         nullable=False)
    
    # user's first & last names - not null
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    
    # user's phone number - unique, not null
    phone_number = db.Column(db.String(15),
                             unique=True,
                             nullable=False)

    # tickets & appointment relationship
    tickets = db.relationship('Ticket',
                              backref='user',
                              lazy=True)

    appointments = db.relationship('Appointment',
                                   backref='user',
                                   lazy=True)
    
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now(timezone.utc))
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Ticket(db.Model):
    '''Class Ticket'''
    id = db.Column(db.Integer,
                   primary_key=True)
    
    title = db.Column(db.Text,
                      nullable=False)
    
    date = db.Column(db.DateTime,
                     nullable=False,
                     default=datetime.now(timezone.utc))

    description = db.Column(db.Text,
                            nullable=False)
    
    status = db.Column(db.String(20),
                       nullable=False,
                       default='Open')

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)

class Appointment(db.Model):
    '''Appointment Class'''
    id = db.Column(db.Integer,
                   primary_key=True)
    
    date = db.Column(db.DateTime,
                     nullable=False)
    
    date_generated = db.Column(db.DateTime,
                               nullable=False,
                               default=datetime.now(timezone.utc))
    
    Time = db.Column(db.Time,
                     nullable=False)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)