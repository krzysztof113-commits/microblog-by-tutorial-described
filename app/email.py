from flask_mail import Message
from app import mail
from threading import Thread
from flask import current_app


def send_async_email(app, msg):
    # Flask uses contexts to avoid having to pass arguments across functions
    # Thread needs application instance in case to work, in overall it's not
    # necessary but in case of custom threads
    # We cannot put current_app here because it is magic function that has
    # proxy server, it would have no value then
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # With this change, the sending of the email will run in the thread,
    # and when the process completes the thread will end and clean itself up.
    Thread(
        target=send_async_email,
        # We need to put current_app here and extract the app instace from it
        args=(current_app._get_current_object(), msg)
    ).start()
