from flask import request, render_template, url_for, redirect, session
from flask_oauthlib.client import OAuth
from flask_oauthlib.provider import OAuth2Provider
from logbook import Logger
from __init__ import app
from forms import UserInfoForm, UserInfoForm2
from models import User

import os


log = Logger()

oauth = OAuth()

# See https://github.com/lepture/flask-oauthlib/blob/master/example/google.py
# for more examples
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


@app.route('/')
def index():
    # access_token = session.get('access_token')
    # if access_token is None:
    #     return redirect(url_for('login'))

    context = dict()

    return render_template('index.html', **context)


@app.route('/user/info', methods=['get', 'post'])
def user_info():
    form = UserInfoForm()

    if form.validate_on_submit():
        return redirect('/user/info/2')

    context = dict(
        form=form,
    )
    return render_template('user/info.html', **context)


@app.route('/user/info/2', methods=['get', 'post'])
def user_info2():
    form = UserInfoForm2()

    if form.validate_on_submit():
        return redirect('/')

    context = dict(
        form=form,
    )
    return render_template('user/info2.html', **context)


@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/authorized')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''

    # TODO: Check whether the user has filled up required information
    # then redirect to an appropriate page

    guser = google.get('userinfo')
    email = guser.data['email']

    if User.check_email(email):
        log.info('A user with an email address <{}> already exists.'.format(
            email))

        return redirect(url_for('index'))

    else:
        log.info('New user <{}>'.format(email))

        keys = (
            # (google user.data key, model user key)
            ('email', 'email'),
            ('family_name', 'family_name'),
            ('given_name', 'given_name'),
            ('id', 'oauth_id'),
        )
        payload = {k[1]: guser.data[k[0]] for k in keys}

        user = User.create(**payload)

        return redirect(url_for('user_info'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
