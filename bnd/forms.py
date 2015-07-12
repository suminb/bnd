# -*- coding: utf8 -*-
from flask_wtf import Form
from wtforms.fields.html5 import EmailField, TelField
from wtforms import Field, StringField, RadioField, SelectField, IntegerField
from wtforms.widgets import ListWidget
from wtforms.validators import DataRequired, NumberRange


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

    birthdate_year = IntegerField(
        'birthdate_year',
        validators=[DataRequired(), NumberRange(min=1900, max=2015)])
    birthdate_month = IntegerField(
        'birthdate_month',
        validators=[DataRequired(), NumberRange(min=1, max=12)])
    birthdate_day = IntegerField(
        'birthdate_day',
        validators=[DataRequired(), NumberRange(min=1, max=31)])

    email = EmailField('email', validators=[DataRequired()])
    phone = TelField('phone', validators=[DataRequired()])
    referrer = StringField('referrer', validators=[])

    question1 = StringField(u'당신의 인생에서 가장 중요한 질문은?')
    question2 = StringField(u'나에게 Being & Doing 이란?')
    question3 = StringField(u'Talk to me about this')


class UserInfoForm2(Form):
    address = StringField('Address', validators=[])
    zipcode = StringField('Zip', validators=[])

    school = StringField('School', validators=[])
    major = StringField('Field of Study', validators=[])
    company = StringField('Company', validators=[])
    title = StringField('Title', validators=[])


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


class CheckpointEvaluationForm(Form):
    attendance = RadioField(
        'attendance',
        choices=[('yes', '예'), ('no', '아니오'), ('na', '해당 없음')],
        validators=[DataRequired()])
    essay = RadioField(
        'attendance',
        choices=[('yes', '예'), ('no', '아니오'), ('na', '해당 없음')],
        validators=[DataRequired()])

    def process(self, formdata=None, obj=None, **kwargs):

        super(CheckpointEvaluationForm, self).process(formdata, obj, kwargs)

        if obj is not None and obj.first() is not None:
            record = obj.first().data
            self.attendance.process(formdata, record['attendance'])
            self.essay.process(formdata, record['essay'])
