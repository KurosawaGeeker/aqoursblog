from flask import render_template,redirect,request,url_for,flash
from . import auth
from flask_login import login_user,logout_user,login_required,current_user
from ..models import User
from .forms import LoginForm
from .forms import RegistrationFrom
import main
from ..import db
from ..email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html',form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经成功登出')
    return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationFrom()
    if form.validate_on_submit():
        user = User(email=form.email.data,cn = form.cn.data,password=form.password.data,mana = form.mana.data)
        db.session.add(user)
        db.session.commit()
        #token = user.generate_confirmation_token()
        #send_email(user.email, 'Confirm Your Account','auth/email/confirm', user=user, token=token)
        #flash('一封验证邮件已经发送到恁邮箱中力')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form = form)

""" #@auth.route('/confirm/<token>') #动态路由界面
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index')) """
""" @auth.before_app_request
def before_request():
    if current_user.is_authenticated() \
        and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.': and request.endpoint != 'static':
    return redirect(url_for('auth.unconfirmed')) #本处出现语法错误，暂时注释掉
 """
""" @auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous() or current_user.confirmed:  #没有验证过的用户
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
 """
""" @auth.route('/confirm')
@login_required #用此装饰器来保护路由，仅登录者才可以访问
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account','auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index')) """

@auth.before_app_request   #更新已登录用户的访问时间
def before_request():
    if current_user.is_authenticated:
            current_user.ping()
"""             if not current_user.confirmed and request.endpoint[:5] != 'auht.':
                return redirect(url_for('auth.unconfirmed')) """