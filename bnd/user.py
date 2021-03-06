from flask import Blueprint, render_template, request, redirect, url_for, \
    session
from flask.ext.login import login_required, login_user, logout_user, \
    current_user
from flask_oauthlib.client import OAuth
from bnd import login_manager, log
from bnd.models import User
from bnd.forms import UserInfoForm, UserInfoForm2
from datetime import datetime

import os


user_module = Blueprint(
    'user', __name__, template_folder='templates/user')


oauth = OAuth()
google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'openid profile email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@user_module.route('/info', methods=['get', 'post'])
@login_required
def edit_info():
    user = current_user
    form = UserInfoForm(request.form, obj=user)

    if user.data is None:
        user.data = {}

    if form.validate_on_submit():
        form.populate_obj(user)

        # FIMXE: Refactor the following statement
        strtime = '{}-{}-{}'.format(form.birthdate_year.data,
                                    form.birthdate_month.data,
                                    form.birthdate_day.data)
        user.birthdate = datetime.strptime(strtime, '%Y-%m-%d')

        keys = ('referrer', 'question1', 'question2', 'question3')

        data = dict(user.data)
        for k in keys:
            data[k] = form.data[k]

        user.data = data
        user.save()

        return redirect('/user/info/2')

    # FIXME: Temporary
    user.data.setdefault('question1', '')
    user.data.setdefault('question2', '')
    user.data.setdefault('question3', '')
    form.question1.data = user.data['question1']
    form.question2.data = user.data['question2']
    form.question3.data = user.data['question3']

    # FIXME: Temporary
    if user.birthdate is not None:
        form.birthdate_year.data = user.birthdate.strftime('%Y')
        form.birthdate_month.data = user.birthdate.strftime('%m')
        form.birthdate_day.data = user.birthdate.strftime('%d')

    context = dict(
        form=form,
    )
    return render_template('user/info.html', **context)


@user_module.route('/info/2', methods=['get', 'post'])
@login_required
def edit_info2():
    user = current_user
    form = UserInfoForm2(request.form, obj=user)

    if user.data is None:
        user.data = {}

    if form.validate_on_submit():
        form.populate_obj(user)

        # keys = ('school', 'major')

        # If the old dict is re-used, the user.data field won't be updated
        data = dict(user.data)
        # for k in keys:
        #     data[k] = form.data[k]

        # FIXME: Temporary
        data['education'] = dict(school=form.data['school'],
                                 major=form.data['major'])
        data['career'] = [dict(company=form.data['company'],
                               title=form.data['title'])]

        user.data = data
        user.save()

        return redirect('/')

    # FIXME: Temporary
    user.data.setdefault('education', dict(school='', major=''))
    form.school.data = user.data['education']['school']
    form.major.data = user.data['education']['major']
    user.data.setdefault('career', [dict(company='', title='')])
    form.company.data = user.data['career'][0]['company']
    form.title.data = user.data['career'][0]['title']

    context = dict(
        form=form,
    )
    return render_template('user/info2.html', **context)


@user_module.route('/login')
def login():
    callback = url_for('user.authorized', _external=True)
    return google.authorize(callback=callback)


@user_module.route('/logout')
def logout():
    session['login'] = False
    logout_user()
    return redirect('/')


@user_module.route('/authorized')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''

    # TODO: Check whether the user has filled up required information
    # then redirect to an appropriate page

    guser = google.get('userinfo')
    email = guser.data['email']

    user = User.get_by_oauth_id(guser.data['id'])

    if user is not None:
        log.info('A user with an email address <{}> already exists.'.format(
            email))
        login_user(user)

        return redirect(url_for('main.index'))

    else:
        log.info('New user <{}>'.format(email))

        keys = (
            # (google user.data key, model user key)
            ('email', 'email'),
            ('family_name', 'family_name'),
            ('given_name', 'given_name'),
            ('id', 'oauth_id'),
            ('picture', 'picture'),
        )
        payload = {k[1]: guser.data[k[0]] for k in keys}

        user = User.create(**payload)
        login_user(user)

        return redirect(url_for('user.edit_info'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')
