# -*- coding: utf8 -*-
from flask_wtf import Form
from wtforms.fields.html5 import EmailField, TelField
from wtforms import Field, StringField, RadioField, DateField, TextAreaField, SelectField
from wtforms import FieldList
from wtforms.widgets import ListWidget
from wtforms.validators import DataRequired


class MultipleRadioFields(Field):
    """A custom field to provide multiple radio button groups."""

    widget = ListWidget()

    def _value(self):
        return ''

    def __iter__(self):
        yield RadioField('test1')
        yield StringField('test3')


class UserInfoForm(Form):
    family_name = StringField('family_name', validators=[DataRequired()])
    given_name = StringField('given_name', validators=[DataRequired()])
    gender = RadioField(
        'gender',
        choices=[('male', 'Male'), ('female', 'Female')],
        validators=[DataRequired()])
    birthdate = DateField('birthdate', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    phone = TelField('phone', validators=[DataRequired()])
    referrer = StringField('referrer', validators=[DataRequired()])

    question1 = StringField(u'당신의 인생에서 가장 중요한 질문은?')
    question2 = StringField(u'나에게 Being & Doing 이란?')
    question3 = StringField(u'Talk to me about this')



class UserInfoForm2(Form):
    education = StringField('Education', validators=[])



class GoalForm(Form):
    type = SelectField(
        u'목표 타입',
        choices=[(u'전공', u'전공'),
                 (u'운동', u'운동'),
                 (u'예술', u'예술'),
                 (u'취미', u'취미'),
                 (u'생활', u'생활'),
                 (u'기타', u'기타')],
        validators=[DataRequired()])
    title = StringField(
        u'목표 내용',
        validators=[DataRequired()])
    criterion1 = StringField(
        '',
        validators=[DataRequired()])
    criterion2 = StringField(
        '',
        validators=[DataRequired()])
    criterion3 = StringField(
        '',
        validators=[DataRequired()])
    criterion4 = StringField(
        '',
        validators=[DataRequired()])
