from . import db
from . import login_manager
from flask_login import UserMixin,login_required,AnonymousUserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer #太长了，利用as可以代替对象名
from . import config 
from flask import current_app
import datetime
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer) #一串数字，各个操作都对应一个位置，能执行操作的角色这个位置会标记为1
    users = db.relationship('User', backref='role',lazy ='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW |Permission.COMMENT |Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |Permission.COMMENT |Permission.WRITE_ARTICLES |Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class User(UserMixin,db.Model): #UserMixin作用详情见P82
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    cn = db.Column(db.String(64),index=True)
    mana = db.Column(db.String(64),index=True)
    email = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean,default=False)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email ==current_app.config['FLASKY_ADMIN']: #如果验证邮箱是管理员的邮箱，则赋予用户全部的权力
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('not readable')

    def generate_confirmation_token(self, expiration=3600): 
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})


    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password): #判断输入密码是否一致，同一个字符串转化为的散列是一样的
        return check_password_hash(self.password_hash,password)
        
    def confirm(self,token): #用户邮箱验证函数
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.load(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True 
    def can(sefl,permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>' % self.cn
class AnonymousUser(AnonymousUserMixin): #匿名用户没有任何权限
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

class Post(db.Model): #文章的模型
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.text)
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader #加载用户的回调函数 接受变量为用户的标识符，如果能找到就返回对象，否则返回none
def load_user(user_id):
    return User.query.get(int(user_id))