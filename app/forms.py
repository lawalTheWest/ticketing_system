''' all forms here in forms.py'''

from wtforms import StringField, PasswordField, SubmitField,  TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    '''the registration form class'''
    username = StringField('Username', validators=[DataRequired(), Length(min=4,max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=4, max=80)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=4,max=80)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Register')

    def validate_username(self, username):
        '''validates username so as to have a unique uname'''
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username not Available!')

    def validate_email(self, email):
        '''validate user.email for uniqueness'''
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email not Available!')
    
    def validate_phone_number(self, phone_number):
        '''Validates phone number to ensure it's unique'''
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user:
            flash('Invalid credentials!')
            raise ValidationError('Phone number already registered!')

class LoginForm(FlaskForm):
    '''Login form received from the user Interface'''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EmailForm(FlaskForm):
    '''the email form class foor account recovery'''
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class TicketForm(FlaskForm):
    '''ticket creation form class'''
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Ticket')
