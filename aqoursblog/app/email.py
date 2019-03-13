from flask_mail import Message
from flask import render_template
from . import config
from flask import current_app

def send_email(to,subject,template,**kwargs):
    msg = Message(config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
