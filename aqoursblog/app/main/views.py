from datetime import datetime
from flask import render_template,session,redirect,url_for,abort,flash,request,current_app,flash
from . import main
from .forms import NameForm
from .forms import EditProfileForm
from .forms import PostForm
from .. import db
from ..models import User,Role,Permission,Post
from .. import auth
from flask_login import current_user,login_required
from .. import config
""" @main.route('/', methods=['GET', 'POST'])
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
    return redirect(url_for('main.index'))
  return render_template('index.html',form = form,cn = session.get('cn'),mana = session.get('mana'),known = session.get('known', False),current_time=datetime.utcnow())
 """
@main.route('/user/<cn>')
def user(cn):
  user = User.query.filter_by(cn = cn).first()
  if user is None:
    abort(404)
  posts = user.posts.order_by(Post.timestamp.desc()).all()
  return render_template('user.html',user=user,posts = posts)

@main.route('/edit-profile', methods=['GET', 'POST']) #用户编辑资料界面
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.mana = form.mana.data
    current_user.location = form.location.data
    current_user.about_me = form.about_me.data
    db.session.add(current_user)
    flash('Your profile has been updated.')
    return redirect(url_for('.user', cn=current_user.cn))
  form.mana.data = current_user.mana
  form.location.data = current_user.location
  form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', form=form)


@main.route('/', methods=['GET', 'POST']) 
def index():
  form = PostForm()
  currentuser = current_user
  if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit(): #如果当前用户拥有写文章权限的话and form.validate_on_submit()
    post = Post(body=form.body.data,author=current_user._get_current_object()) #实例化
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('.index'))
  #else:
    #return render_template('404.html')  #没有权限，测试语句，直接返回404，权限问题还需要另外确定
  posts = Post.query.order_by(Post.timestamp.desc()).all()  #完整的博客文章列表传给 以时间戳进行降序排序
  page = request.args.get('page',1,type = int)
  pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page,per_page=config.FLASK_POSTS_PER_PAGE,error_out=False)
  #error_out=true 会在超出页面的时候报错
  #重要坑，导入config，以.来引用config下的变量，config此时不是字典，而是一个模型
  posts = pagination.items
  return render_template('index.html',form = form,posts = posts,currentuser=currentuser,pagination=pagination)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id) #查询对应的id值
    return render_template('post.html',posts=[post])



@main.route('/edit_post/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
  form = PostForm()
  post = Post.query.get_or_404(id)
  if current_user != post.author and current_user.can(Permission.ADMINISTER):
    abort(403)
  if form.validate_on_submit():
    post.body = form.body.data
    db.session.add(post)
    flash('你的文章已经更新')
    return redirect(url_for('.post',id=post.id))
  form.body.data = post.body
  return render_template('edit_post.html',form=form)
