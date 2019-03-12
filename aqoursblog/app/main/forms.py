from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import  Required,Email,Length


class LoginForm(Form):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('密码',validators=[Required()])
    remember_me = BooleanField('要我一直保持登录吗')
    submit = SubmitField('登录')

class NameForm(Form):
    cn = StringField('恁滴圈名是?',validators=[Required()])#cn 必填
    mana = StringField('你滴名字是啥？（真 名 爆 破）') #非必填
    submit = SubmitField('Submit')

class EditProfileForm(Form):
    mana = StringField('真名',validators=[Length(0, 64)])
    location =  StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class PostForm(Form):
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')