
import smtplib, ssl
import os

import smtplib
import ssl
from email.message import EmailMessage


def sendEmail(receiver_email, message):

    email_sender = os.environ.get("email")
    email_password = os.environ.get("password")
    email_receiver = receiver_email
    subject = 'Thankyou for shopping'
    body = message

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())