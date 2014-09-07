from flask_wtf import Form
from flask_wtf.html5 import EmailField, TelField
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

