# utils/pdf_generator.py

from fpdf import FPDF
from flask import make_response

def generate_ticket_pdf(ticket, user):
    """
    Generates a PDF for a ticket, displaying user and ticket details.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Set font for the PDF
    pdf.set_font("Arial", "B", 12)

    # Business Name (Header)
    pdf.cell(200, 10, txt=user.business_name, ln=True, align="C")
    pdf.ln(10)

    # Attending Officer Information
    pdf.set_font("Arial", "B", 10)
    pdf.cell(200, 10, txt="Official Contacts / Details", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Attending Officer: {user.first_name} {user.last_name}", ln=True)
    pdf.cell(200, 10, txt=f"Officer ID: {user.id}", ln=True)
    pdf.cell(200, 10, txt=f"Company Email: {user.email}", ln=True)
    pdf.cell(200, 10, txt=f"Company Phone: {user.phone_number}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Client Details", ln=True)
    pdf.ln(5)
    
    # Ticket Information
    pdf.set_font("Arial", "B", 10)
    pdf.cell(200, 10, txt="Ticket Information", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"First Name: {ticket.client_first_name}", ln=True)
    pdf.cell(200, 10, txt=f"Last Name: {ticket.client_last_name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {ticket.client_email}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {ticket.client_phone_number}", ln=True)
    pdf.cell(200, 10, txt=f"Ticket ID: {ticket.id}", ln=True)
    pdf.cell(200, 10, txt=f"Title: {ticket.title}", ln=True)
    pdf.cell(200, 10, txt=f"Description: {ticket.description}", ln=True)
    pdf.cell(200, 10, txt=f"Status: {ticket.status}", ln=True)
    pdf.cell(200, 10, txt=f"Event Date: {ticket.event_date.strftime('%Y-%m-%d')}", ln=True)
    pdf.cell(200, 10, txt=f"Date Generated: {ticket.date.strftime('%Y-%m-%d')}", ln=True)
    
    # Return the generated PDF as a Flask response
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers.set('Content-Disposition', f'attachment; filename=ticket_{ticket.id}.pdf')
    response.headers.set('Content-Type', 'application/pdf')
    
    return response