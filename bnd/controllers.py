from flask import render_template, url_for, redirect, session
from flask_oauthlib.client import OAuth
from logbook import Logger
from __init__ import app
from forms import UserInfoForm

import os


log = Logger()

oauth = OAuth()

google = oauth.remote_app(
    'google',
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email'
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

    # if google.has('userinfo'):
    #     me = google.get('userinfo')
    #     print(me)

    context = dict()

    return render_template('index.html', **context)


@app.route('/user/info', methods=['get', 'post'])
def user_info():
    form = UserInfoForm()

    if form.validate_on_submit():
        return redirect('/user/info?page=2')

    context = dict(
        form=form,
    )
    return render_template('user/info.html', **context)


@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/authorized')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
