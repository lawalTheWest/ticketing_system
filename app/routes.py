#!/usr/bin/env python3
# app/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm, TicketForm, EmailForm, AppointmentForm, RescheduleTicketForm, EditProfileForm
from . import db, bcrypt
from .base_model import User, Ticket, Appointment
from datetime import date, datetime, timezone
from werkzeug.utils import secure_filename
import os
from fpdf import FPDF
from .utils.pdf_generator import generate_ticket_pdf


routes = Blueprint('routes', __name__)



'''
    Home route
'''
@routes.route('/')
def Home():
    '''Defines the home function'''
    return render_template("home.html")



'''
    about routes
'''
@routes.route('/about')
def About():
    '''defines the about function'''
    return render_template('about.html')




'''
    User authentication
'''



'''
    Login route
'''
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




'''
    register route
'''
@routes.route('/register', methods=['GET', 'POST'])
def Register():
    '''define registration function and its logics'''
    form = RegisterForm()

    '''validate credentials'''
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        filename = None

        if form.profile_picture.data:
            profile_picture_file = form.profile_picture.data
            # Validating file type for security purposes
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
            if not ('.' in profile_picture_file.filename and profile_picture_file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
                flash('Invalid file type for profile picture. Only images are allowed.', 'danger')
                return redirect(url_for('routes.Register'))

            # Create a safe filename
            filename = secure_filename(profile_picture_file.filename)

            '''make the path to save the profile picture and save it in the directory'''
            file_path = os.path.join(current_app.root_path, 'static/profile_pics', filename)
            profile_picture_file.save(file_path)

        '''Check uniqueness for phone number'''
        existing_user = User.query.filter_by(phone_number=form.phone_number.data).first()
        if existing_user:
            flash('Phone number is already registered. Please use a different number.', 'danger')
            return redirect(url_for('routes.Register'))

        '''create new user instance'''
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        business_name=form.business_name.data,
                        profile_picture=filename,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        phone_number=form.phone_number.data,
                        # password=hashed_password
                        )
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Account Created Successfully! You can now log in.', 'success')
        print(f"File saved to {file_path}")
        return redirect(url_for('routes.Login'))
    
    return render_template('register.html', form=form)




'''
    logout route
'''
@routes.route('/logout', methods=['GET', 'POST'])
@login_required
def Logout():
    '''logs user out of the session'''
    logout_user()
    flash('Logged out Successfully!', 'info')
    return redirect(url_for('routes.Home'))




'''
    dashboard route
'''
@routes.route('/dashboard', methods=['GET', 'POST'])
@login_required
def Dashboard():
    return render_template('dashboard.html')



'''
    edit profile
'''
@routes.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''Allow user to edit their profile'''
    form = EditProfileForm()

    # Pre-fill the form with current user details
    if request.method == 'GET':
        form.username.data = current_user.username
        form.business_name.data = current_user.business_name
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone_number.data = current_user.phone_number

    if form.validate_on_submit():
        if form.profile_picture.data:
            profile_picture_file = form.profile_picture.data
            # Validating and saving profile picture
            filename = secure_filename(profile_picture_file.filename)
            file_path = os.path.join(current_app.root_path, 'static/profile_pics', filename)
            profile_picture_file.save(file_path)
            current_user.profile_picture = filename

        current_user.username = form.username.data
        current_user.business_name = form.business_name.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone_number = form.phone_number.data

        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('routes.Dashboard'))

    return render_template('edit_profile.html', form=form)


'''
    Creating the tickets
'''
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
        new_ticket = Ticket(title=request.form.get('title'), 
                            event_date=form.event_date.data,
                            user_id=current_user.id,
                            description=request.form.get('description'),
                            status=request.form.get('status'),
                            
                            # client_first_name=form.client_first_name,

                            client_first_name=request.form.get('client_first_name'),
                            client_last_name=request.form.get('client_last_name'),
                            client_email=request.form.get('client_email'),
                            client_phone_number=request.form.get('client_phone_number')
                            )
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

'''View individual ticket'''
@routes.route('/ticket/<int:ticket_id>', methods=['GET'])
@login_required
def View_ticket(ticket_id):
    '''
        View a single ticket by ticket_id.
        Ensures that the ticket is only viewable by the user who created it.
    '''
    # Fetch the ticket from the database using the ticket_id
    ticket = Ticket.query.get_or_404(ticket_id)

    # Ensure that the current user is the one who created the ticket
    if ticket.user_id != current_user.id:
        flash("You do not have permission to view this ticket.", "danger")
        return redirect(url_for('routes.View_tickets'))

    # Fetch the user's details
    user = User.query.get(ticket.user_id)

    # Render the ticket details page
    return render_template('view_ticket.html', ticket=ticket, user=user)


'''Reschedule tickets'''
@routes.route('/reschedule_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def Reschedule_ticket(ticket_id):
    '''logic for rescheduling a ticket'''
    # Fetch the ticket from the database using the ticket_id
    form = RescheduleTicketForm()

    ticket = Ticket.query.get_or_404(ticket_id)

    if  request.method == 'POST':  # and form.validate_on_submit():
        # if form.validate_on_submit(): 
        new_date = form.new_date.data  # This will return a 'date' object

        # Convert 'new_date' (date object) to a 'datetime' object with time set to 00:00:00
        new_datetime = datetime.combine(new_date, datetime.min.time(), tzinfo=timezone.utc)

        # Update the ticket with the new schedule
        ticket.event_date = new_datetime
        ticket.status = 'Closed' if new_datetime < datetime.now(timezone.utc) else 'Open'

        db.session.commit()

        flash('Ticket rescheduled successfully!', 'success')
        return redirect(url_for('routes.View_tickets'))

    return render_template('reschedule_ticket.html', form=form, ticket=ticket)


'''Cancel tickets'''
@routes.route('/cancel_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def Cancel_ticket(ticket_id):
    ''' logics for cancelling a ticket'''

    '''Fetch the ticket from the database using the ticket_id'''
    ticket = Ticket.query.get_or_404(ticket_id)

    '''update the ticket status to canceled'''
    ticket.status = 'canceled'

    db.session.commit()

    flash('Ticket canceled successfully!', 'success')
    return redirect(url_for('routes.View_tickets'))


'''deleting a ticket'''
@routes.route('/delete_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def Delete_ticket(ticket_id):
    ''' logics for deleting a ticket'''

    '''Fetch the ticket from the database using the ticket_id'''
    ticket = Ticket.query.get_or_404(ticket_id)

    '''deletes ticket'''
    db.session.delete(ticket)

    db.session.commit()

    flash('Ticket deleted successfully!', 'success')
    return redirect(url_for('routes.View_tickets'))



'''
    THE FPDF SECTION TO GENERATE
'''

@routes.route('/download_ticket/<int:ticket_id>', methods=['GET'])
@login_required
def download_ticket(ticket_id):
    """
        Route to generate and download the PDF for a specific ticket.
    """
    # Fetch the ticket and user from the database
    ticket = Ticket.query.get_or_404(ticket_id)
    user = User.query.get_or_404(ticket.user_id)

    # Ensures the current user is authorized to download the ticket
    if user.id != current_user.id:
        '''abort - Forbidden'''
        abort(403)

    # Generate the PDF and return it as a downloadable response
    return generate_ticket_pdf(ticket, user)








'''
    Appointment booking section
'''
@routes.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    '''defines the routes for appointment booking functionality'''
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment_date = datetime.combine(form.date.data, form.time.data)

        # Check for conflicts
        conflicting_appointments = Appointment.query.filter_by(
            user_id=current_user.id, date=form.date.data
        ).filter(Appointment.time == form.time.data).first()
        
        if conflicting_appointments:
            flash('This time slot is already booked for another appointment. Please choose another time.', 'danger')
            return redirect(url_for('routes.book_appointment'))

        # If no conflict, create appointment
        new_appointment = Appointment(
            date=appointment_date, 
            time=form.time.data, 
            user_id=current_user.id, 
            purpose=form.purpose.data
        )
        db.session.add(new_appointment)
        db.session.commit()

        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('routes.view_appointments'))

    return render_template('book_appointment.html', form=form)


@routes.route('/view_appointments', methods=['GET'])
@login_required
def view_appointments():
    '''View all appointments for the current user'''
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('view_appointments.html', appointments=appointments)


@routes.route('/cancel_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def cancel_appointment(appointment_id):
    '''Cancel an appointment'''
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if the user is allowed to cancel this appointment
    if appointment.user_id != current_user.id:
        flash('You are not authorized to cancel this appointment.', 'danger')
        return redirect(url_for('routes.view_appointments'))

    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment cancelled successfully.', 'success')
    return redirect(url_for('routes.view_appointments'))

@routes.route('/reschedule_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def reschedule_appointment(appointment_id):
    '''Reschedule an appointment'''
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Ensure the user owns this appointment
    if appointment.user_id != current_user.id:
        flash('You are not authorized to reschedule this appointment.', 'danger')
        return redirect(url_for('routes.view_appointments'))

    form = AppointmentForm()
    
    if form.validate_on_submit():
        new_date = datetime.combine(form.date.data, form.time.data)

        # Check for conflicts
        conflicting_appointments = Appointment.query.filter_by(
            user_id=current_user.id, date=form.date.data
        ).filter(Appointment.time == form.time.data).first()

        if conflicting_appointments:
            flash('This time slot is already booked for another appointment. Please choose another time.', 'danger')
            return redirect(url_for('routes.reschedule_appointment', appointment_id=appointment_id))

        # Update the appointment details
        appointment.date = new_date
        appointment.time = form.time.data
        appointment.purpose = form.purpose.data
        db.session.commit()

        flash('Appointment rescheduled successfully!', 'success')
        return redirect(url_for('routes.view_appointments'))

    return render_template('reschedule_appointment.html', form=form, appointment=appointment)