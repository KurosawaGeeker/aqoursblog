from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('Password',validators=[Required()])
    remember_me = BooleanField('Keep me logged in') #是否保持登录状态
    submit = SubmitField('Log In')

class RegistrationFrom(Form):
    cn = StringField('恁滴圈名是?',validators=[Required()])#cn 必填
    mana = StringField('你滴名字是啥？（真 名 爆 破）') #非必填
    email = StringField('邮箱',validators=[Required(), Length(1,64),Email()])
    password = PasswordField('设置密码', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('确认密码', validators=[Required()]) #不相同无法提交
    submit = SubmitField('Register')
    def validate_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('这个邮箱已经被注册.')
    def validate_cn(self,field):
        if User.query.filter_by(cn=field.data).first():
            raise ValidationError('你这个圈名太土了，被注册了')