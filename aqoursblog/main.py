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
import flask_shell
import pymysql
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YES@localhost/test2'
app.config['SQCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com' #电邮的主机名
app.config['MAIL_PORT'] = 587 #电子邮件服务器的端口
app.config['MAIL_USE_TLS'] = True  #启用传输层安全协议
app.config['MAIL_USERNAME'] = 'wuyajungood@126.com' #邮件账户的用户名
app.config['MAIL_PASSWORD'] = '*13181463590'#密码
app.config['MAIL_DEFAULT_SENDER']='wuyajungood@126.com'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'wuyajungood@126.com'
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(64), unique=True)
  users = db.relationship('User', backref='role')
  def __repr__(self):
    return '<Role %r>' % self.name
class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer,primary_key=True)
  cn = db.Column(db.String(64),index=True)
  mana = db.Column(db.String(64),index=True)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  def __repr__(self):
    return '<User %r>' % self.cn

class NameForm(Form):
    cn = StringField('恁滴圈名是?',validators=[Required()])#cn 必填
    mana = StringField('你滴名字是啥？（真 名 爆 破）') #非必填
    submit = SubmitField('Submit')

def make_shell_context():
  return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))

""" def send_email(to, subject, template, **kwargs):
  msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
  msg.body = render_template(template + '.txt', **kwargs)
  msg.html = render_template(template + '.html', **kwargs)
  mail.send(msg) """

@app.route('/', methods=['GET', 'POST'])
def index():
  form = NameForm()
  
  if form.validate_on_submit():
    user = User.query.filter_by(cn=form.cn.data).first()
    if user :
      session['known']=True
    else:
      user = User(cn = form.cn.data)
      db.session.add(user)
      session['known']=False
      if app.config['FLASKY_ADMIN']:
        send_email(app.config['FLASKY_ADMIN'], 'New User','mail/new_user', user=user)
    session['cn'] = form.cn.data
    session['mana'] = form.mana.data
    form.cn.data = ''
    form.mana.data = ''
    return redirect(url_for('index'))
  return render_template('index.html',form = form,cn = session.get('cn'),mana = session.get('mana'),known = session.get('known', False),current_time=datetime.utcnow())
@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
  
if __name__ == '__main__':
    #app.run(host='localhost', port=5000)
    print("It is my own invention")
    manager.run()
    