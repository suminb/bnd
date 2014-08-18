from flask import Flask, render_template, url_for, redirect, session
from flask_oauth import OAuth

GOOGLE_CLIENT_ID = '169743770999-fr1pv3hmkrlmhb959ogu3l0utebfe0kg.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'BlQ5zkY1GPfrdqgks0EhFVHO'

app = Flask(__name__)
app.secret_key = 'asdf'
oauth = OAuth()

google = oauth.remote_app('google',
            base_url='https://www.google.com/accounts/',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            request_token_url=None,
            request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                'response_type': 'code'},
            access_token_url='https://accounts.google.com/o/oauth2/token',
            access_token_method='POST',
            access_token_params={'grant_type': 'authorization_code'},
            consumer_key=GOOGLE_CLIENT_ID,
            consumer_secret=GOOGLE_CLIENT_SECRET)


@app.route('/')
def index():
    # access_token = session.get('access_token')
    # if access_token is None:
    #     return redirect(url_for('login'))

    return render_template('index.html')


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
