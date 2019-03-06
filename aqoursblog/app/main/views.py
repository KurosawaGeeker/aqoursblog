from datetime import datetime
from flask import render_template,session,redirect,url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from .. import auth

@main.route('/', methods=['GET', 'POST'])
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


