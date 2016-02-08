# Functions for sending emails from NameNest.
#
# Functions:
#   send_email - send an email from NameNest.
#   send_async_email - create a thread to send an asynchronous email.

from threading import Thread

from flask import current_app, render_template
from flask.ext.mail import Message

from . import mail


def send_email(app, msg):
    # Send a message from this app. App context is required since
    # message is being sent in a thread.
    #
    # Arguments:
    #   app (Flask) - provides the application context for
    #                 sending the message.
    #   msg (string) - a Message object. This must have a send() method.
    #
    # Raises:
    #  RuntimeError - when working outside the application context
    #  ???

    with app.app_context():
        mail.send(msg)


def send_async_email(recipient, subject, template, **context):
    # Prepare a thread to send an email to a given recipient
    # asynchronously.
    #
    # Arguments:
    #   recipient (string): email address of the recipient.
    #   subject (string): the subject of the email.
    #   template (string): filename of the text / html of the email
    #   ---------- OPTIONAL ----------
    #   context (dictionary):
    #       dictionary of variables that should be available in the
    #       context of a template.
    #
    # Returns:
    #   (Thread) - the thread responsible for sending the email.
    #
    # Raises:
    #   RuntimeError - when working outside the application context
    #   ???

    # Set up the application context and build the message.
    app = current_app._get_current_object()
    msg = Message(
        app.config['NAMENEST_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender=app.config['NAMENEST_MAIL_SENDER'],
        recipients=[recipient]
    )
    msg.body = render_template(template + '.txt', **context)
    msg.html = render_template(template + '.html', **context)

    # Start a thread to send the email.
    thread = Thread(target=send_email, args=[app, msg])
    thread.start()

    return thread
