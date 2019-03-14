from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail
from app import create_app,db
from flask_login import login_required

import pymysql
import os
from app.models import User,Role,Post
import config
basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
manager = Manager(app)
DEBUG = False

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

""" @app.route('/secret')
@login_required
def secret():
  return 'Only authenticated users are allowed'
 """#保护路由，未认证的用户无法访问该secret路由，secret可以替换


def make_shell_context():
  return dict(app=app,db=db,User=User,Role=Role,Post=Post)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

""" def send_email(to, subject, template, **kwargs):
  msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
  msg.body = render_template(template + '.txt', **kwargs)
  msg.html = render_template(template + '.html', **kwargs)
  mail.send(msg) """

if __name__ == '__main__':
    #app.run(host='localhost', port=5000)
    print("It is my own invention")
    manager.run()
    