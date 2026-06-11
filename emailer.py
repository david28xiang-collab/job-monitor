import os
import smtplib
from email.mime.text import MIMEText


def send_email(subject, body):

    sender = os.environ["EMAIL_ADDRESS"]
    password = os.environ["EMAIL_PASSWORD"]

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = sender

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender,
            password
        )

        server.send_message(msg)