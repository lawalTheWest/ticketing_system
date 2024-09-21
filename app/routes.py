#!/usr/bin/env python3
# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, TicketForm, EmailForm
from wtforms import StringField, PasswordField, SubmitField,  TextAreaField, SelectField, DateField
from . import db, bcrypt
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from .base_model import User, Ticket
from datetime import date
import app

routes = Blueprint('routes', __name__)

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
    '''Defines the function to the ticket page'''
    return render_template('ticket_page.html')

@routes.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def Create_ticket():
    '''Defines the function to create new tickets'''
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
    '''
        Defines the function to view all tickets created:
            - Closed tickets and
            - Opened tickets
    '''
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    for ticket in tickets:
        ticket.update_status()
    db.session.commit()
    return render_template('view_tickets.html', tickets=tickets)
