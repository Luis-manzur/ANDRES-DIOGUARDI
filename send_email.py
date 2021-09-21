import smtplib, ssl
import os

def send_email(name, email, phone_number, message):
    email_message = f"""
    Name: {name}
    Email: {email}
    Phone Number: {phone_number}
    Message: {message}
    """

    email_sender = os.environ.get('EMAIL_SENDER')
    email_password = os.environ.get('EMAIL_PASSWORD')
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_sender, email_message)

