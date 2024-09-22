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
    __tablename__ = 'users'

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
                              backref='creator',
                              lazy=True)

    appointments = db.relationship('Appointment',
                                   backref='creator',
                                   lazy=True)
    
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now(timezone.utc))
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

from datetime import date

class Ticket(db.Model, UserMixin):
    '''Ticket class'''
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    date = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now(timezone.utc))

    event_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Open')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Ticket {self.id} - {self.title}>'

    def update_status(self):
        '''Logic to update ticket status based on current date and event date'''
        current_time = datetime.now(timezone.utc)

        '''Ensuring that both dates are compared as datetime objects'''
        if self.status != 'canceled' and self.event_date:
            if isinstance(self.event_date, datetime):
                '''
                    If event_date includes time,
                    compare it directly with the current_time
                '''
                if self.event_date < current_time and self.status == 'open':
                    self.status = 'closed'
                    db.session.commit()
            else:
                '''
                    If event_date is a date object,
                    convert current_time to date for comparison
                '''
                if self.event_date < current_time.date() and self.status == 'open':
                    self.status = 'closed'
                    db.session.commit()


'''
    The Appointment Model
'''
class Appointment(db.Model, UserMixin):
    '''Appointment Class'''
    __tablename__ = 'appointments'

    id = db.Column(db.Integer,
                   primary_key=True)
    
    date = db.Column(db.DateTime,
                     nullable=False)
    
    date_generated = db.Column(db.DateTime,
                               nullable=False,
                               default=datetime.now(timezone.utc))
    
    time = db.Column(db.Time,
                     nullable=False)
    
    status = db.Column(db.String(10), nullable=False, default='Upcoming')

    
    purpose = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    def update_status(self):
        ''' Automatically updates the status based on the event date '''
        if self.event_date < date.today():
            self.status = 'passed'
        else:
            self.status = 'Upcoming'