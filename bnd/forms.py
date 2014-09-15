from flask_wtf import Form
from wtforms.fields.html5 import EmailField, TelField
from wtforms import StringField, RadioField, DateField
from wtforms.validators import DataRequired


class UserInfoForm(Form):
    family_name = StringField('family_name', validators=[DataRequired()])
    given_name = StringField('given_name', validators=[DataRequired()])
    gender = RadioField(
        'gender',
        choices=[('male', 'Male'), ('female', 'Female')],
        validators=[DataRequired()])
    birthdate = DateField('birthdate', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    phone = TelField('phone')
    referrer = StringField('referrer', validators=[DataRequired()])
    education = StringField('Education', validators=[])


class UserInfoForm2(Form):
    question1 = StringField(u'당신의 인생에서 가장 중요한 질문은?')
    question2 = StringField(u'나에게 Being & Doing 이란?')
    question3 = StringField(u'Talk to me about this')
