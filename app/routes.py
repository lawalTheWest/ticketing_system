#!/usr/bin/env python3
# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from wtforms import StringField, PasswordField, SubmitField,  TextAreaField, SelectField, DateField
from . import db, bcrypt
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from .base_model import User, Ticket
from datetime import date
# from flask_mail import Message
# from itsdangerous import URLSafeTimedSerializer as Serializer
# from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import app

routes = Blueprint('routes', __name__)

'''Registration form'''
class RegisterForm(FlaskForm):
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
# class TicketForm(FlaskForm):
    # title = StringField('Title', validators=[DataRequired()])
    # description = TextAreaField('Description', validators=[DataRequired()])
    # date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    # event_date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    # submit = SubmitField('Create Ticket')

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = DateField('Event Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create Ticket')

'''Home route'''
@routes.route('/')
def Home():
    '''Defines the home function'''
    return render_template("home.html")

'''about routes'''
@routes.route('/about')
def About():
    '''defines the about function'''
    return render_template('about.html')

'''Login route'''
@routes.route('/login', methods=['GET', 'POST'])
def Login():
    '''defines the login function and it logics'''
    form = LoginForm()
    
    '''Check if the form is submitted and is valid'''
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        '''Check if user credential exist in the db'''
        if user:
            '''check the hash'''
            if user.check_password(form.password.data):
                '''log user in'''
                login_user(user)
                flash('Logged in Successfulyy', 'success')
                return redirect(url_for('routes.Dashboard'))
            else:
                '''if password check fails'''
                flash('Invalid Email or Password', 'danger')
        else:
            '''If user is not found'''
            flash('User Not Found!', 'danger')
    
    '''Renders the login page if there is any error with validation'''
    return render_template('login.html', form=form)

'''register route'''
@routes.route('/register', methods=['Get', 'Post'])
def Register():
    '''define registration function and its logics'''
    form = RegisterForm()

    '''validate credentials'''
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        phone_number=form.phone_number.data)
        new_user.set_password(form.password.data)
        # Check uniqueness for phone number
        existing_user = User.query.filter_by(phone_number=form.phone_number.data).first()
        if existing_user:
            flash('Phone number is already registered. Please use a different number.', 'danger')
            return redirect(url_for('routes.Register'))

        db.session.add(new_user)
        db.session.commit()
        flash('Account Created Successfully! You can now Log in.', 'success')
        return redirect(url_for('routes.Login'))
    return render_template('register.html', form=form)

'''logout route'''
@routes.route('/logout', methods=['GET', 'POST'])
@login_required
def Logout():
    '''logs user out of the session'''
    logout_user()
    flash('Logged out Successfully!', 'info')
    return redirect(url_for('routes.Home'))

'''dashboard route'''
@routes.route('/dashboard', methods=['GET', 'POST'])
@login_required
def Dashboard():
    return render_template('dashboard.html')


'''Creating the tickets'''
@routes.route('/ticket_page')
def Ticket_page():
    return render_template('ticket_page.html')

# @routes.route('/create_ticket', methods=['GET', 'POST'])
# @login_required
# def Create_ticket():
#     form = TicketForm()
#     if form.validate_on_submit():
#         # Determine the status based on event date
#         status = 'Closed' if form.event_date.data < date.today() else 'Open'

#         '''Create new ticket'''
#         new_ticket = Ticket(
#             title=form.title.data,
#             description=form.description.data,
#             event_date=form.event_date.data,
#             date=form.date.data,
#             status=status,  # Set the initial status
#             user_id=current_user.id  # Set the current user's ID
#         )
#         try:
#             db.session.add(new_ticket)
#             db.session.commit()
#             flash('Ticket created successfully!', 'success')
#             return redirect(url_for('routes.View_tickets'))
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error creating ticket: {str(e)}', 'danger')
#             return redirect(url_for('routes.Create_ticket'))
#     return render_template('create_ticket.html', form=form)

# @routes.route('/tickets')
# @login_required
# def View_tickets():
#     # Fetch all tickets from the database
#     tickets = Ticket.query.all()

#     # Update the status of each ticket based on the event date
#     for ticket in tickets:
#         ticket.update_status()

#     # Commit any status changes to the database
#     db.session.commit()

#     return render_template('view_tickets.html', tickets=tickets)



@routes.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def Create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        status = 'Closed' if form.event_date.data < date.today() else 'Open'
        new_ticket = Ticket(title=form.title.data, description=form.description.data, 
                            event_date=form.event_date.data, status=status, 
                            user_id=current_user.id)
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('routes.View_tickets'))
    return render_template('create_ticket.html', form=form)

'''View all tickets route'''
@routes.route('/tickets')
@login_required
def View_tickets():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    for ticket in tickets:
        ticket.update_status()
    db.session.commit()
    return render_template('view_tickets.html', tickets=tickets)
