from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import  Required,Email
from flask_wtf import FlaskForm

class NameForm(FlaskForm):
    cn = StringField('恁滴圈名是?',validators=[Required()])#cn 必填
    mana = StringField('你滴名字是啥？（真 名 爆 破）') #非必填
    submit = SubmitField('Submit')