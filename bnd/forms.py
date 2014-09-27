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
    phone = TelField('phone')
    referrer = StringField('referrer', validators=[DataRequired()])
    education = StringField('Education', validators=[])


class UserInfoForm2(Form):
    question1 = StringField(u'당신의 인생에서 가장 중요한 질문은?')
    question2 = StringField(u'나에게 Being & Doing 이란?')
    question3 = StringField(u'Talk to me about this')


class ApplicationForm(Form):
    question1 = RadioField(
        'Member로 연속 2번 참여시, 3번째는 chair를 맡아야 함을 알고 있습니까?',
        choices=[('na', '알고 있습니다. 해당 사항이 없습니다.'),
                 ('positive', '알고 있습니다. 지원할 예정입니다.'),
                 ('exception', '알고 있습니다. 다만 개인적인 사정으로 member로 참여할 예정입니다.')],
        validators=[DataRequired()]
    )
    question2 = RadioField(
        'Chair/member 중 어떻게 지원하십니까?',
        choices=[('chair-1', 'Chair 못 할 시, member 로 참여'),
                 ('chair-2', 'Chair 못 할 시, 다음 기수로 참여'),
                 ('member-1', 'Member (재참여), 하지만 chair 가능'),
                 ('member-2', 'Member (재참여)'),
                 ('member-3', 'Member (신규참여)')],
        validators=[DataRequired()]
    )
    question3 = StringField(
        'Being & Doing 이라는 모임을 파악하기 위해 투자한 시간은 얼마입니까?',
        validators=[DataRequired()]
    )
    question4 = TextAreaField(
        'Being & Doing은 어떤 모임입니까?',
        validators=[DataRequired()]
    )
    #question5 = MultipleRadioFields('개인이 원하는 삶을 살기 위해 중요한 것은 무엇입니까?')


class GoalForm(Form):
    type = SelectField(u'목표 타입',
        choices=[('전공', '전공')],
        validators=[DataRequired()])
    title = StringField(u'목표 내용')
