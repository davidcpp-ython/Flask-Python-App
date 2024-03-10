from . import mail
from flask_mail import Message
import re

def is_valid_email(email):
    
    email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    match = email_pattern.match(email)

    return bool(match)



def send_emergency_notification(patient):
    subject = f'Emergency Notification for {patient.patient_name}'
    body = f"Dear {patient.contact},\n\nThis mail has been sent to you so you know that {patient.patient_name} has been marked as an emergency.\nTake Care,\nOur Emergency App"

    msg = Message(subject, recipients=[patient.contact], body=body)
    mail.send(msg)