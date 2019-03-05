from . import db
from . import login_manager
from flask_login import UserMixin,login_required
from werkzeug.security import generate_password_hash,check_password_hash


class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer,primary_key=True)
  name = db.Column(db.String(64), unique=True)
  users = db.relationship('User', backref='role')
  def __repr__(self):
    return '<Role %r>' % self.name

class User(UserMixin,db.Model): #UserMixin作用详情见P82
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    cn = db.Column(db.String(64),index=True)
    mana = db.Column(db.String(64),index=True)
    email = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('not readable')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password): #判断输入密码是否一致，同一个字符串转化为的散列是一样的
        return check_password_hash(self.password_hash,password)
        
    def __repr__(self):
        return '<User %r>' % self.cn

@login_manager.user_loader #加载用户的回调函数 接受变量为用户的标识符，如果能找到就返回对象，否则返回none
def load_user(user_id):
    return User.query.get(int(user_id))