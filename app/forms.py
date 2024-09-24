''' all forms here in forms.py'''

from flask import flash
from wtforms import StringField, PasswordField, SubmitField,  TextAreaField, SelectField, DateField, TimeField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from datetime import datetime
from .base_model import User
from flask_wtf.file import FileAllowed

class RegisterForm(FlaskForm):
    '''the registration form class'''
    username = StringField('Username', validators=[DataRequired(), Length(min=4,max=80)])
    business_name = StringField('Business Name', validators=[DataRequired(), Length(min=1, max=200)])
    profile_picture = FileField('Business Logo / Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
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
    client_first_name = StringField('Client First Name', validators=[DataRequired()])
    client_last_name = StringField('Client Last Name', validators=[DataRequired()])
    client_middle_name = StringField('Client Middle Name', validators=[DataRequired()])
    client_email = StringField('Client Email', validators=[DataRequired(), Email()])
    client_phone_number = StringField('Client Phone Number', validators=[DataRequired()])
    submit = SubmitField('Create Ticket')

class RescheduleTicketForm(FlaskForm):
    new_date = DateField('New Schedule Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Reschedule Ticket')

class AppointmentForm(FlaskForm):
    '''Form for creating appointments'''
    date = DateField('Appointment Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Appointment Time', format='%H:%M', validators=[DataRequired()])
    purpose = TextAreaField('Purpose of Appointment', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

    def validate_date(self, date):
        '''Check if the appointment is in the future'''
        if date.data < datetime.now().date():
            raise ValidationError('Appointment date must be in the future.')

    def validate_time(self, time):
        '''Ensure the time is valid'''
        if datetime.combine(self.date.data, time.data) < datetime.now():
            raise ValidationError('Appointment time must be in the future.')