# user endpoint
# database

import os
from functools import wraps

from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth, OAuthException

# from models.models import db

# import matching
# from users import fetch_users
# from models import User
# from models import matching
# from models.users import fetch_users
# from src.models.models import User

app = Flask(__name__)

# APP_SETTINGS picked up from autoenv and .env file
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Sanity Checker for env variables
print('Environment configuration is: {}'.format( os.environ['APP_SETTINGS']) )
print('RC_CLIENT_ID', os.environ.get('RC_CLIENT_ID', ''))
print('RC_SECRET', os.environ.get('RC_SECRET', ''))


oauth = OAuth(app)
rc_auth = oauth.remote_app(

    # for local

    # 'recurse_center',
    # base_url='https://www.recurse.com/api/v1/',
    # access_token_url='https://www.recurse.com/oauth/token',
    # authorize_url='https://www.recurse.com/oauth/authorize',
    # consumer_key=os.environ.get('RC_CLIENT_ID', None),
    # consumer_secret=os.environ.get('RC_SECRET', None),
    # access_token_method='POST')rc_auth = oauth.remote_app(

    # for online dev

    'recurse_center',
    base_url='https://www.recurse.com/api/v1/',
    access_token_url='https://www.recurse.com/oauth/token',
    authorize_url='https://www.recurse.com/oauth/authorize',
    consumer_key= 'f1e02c84e292da0bd2b6bd19236f2c69a4a4a69b22e7090137eafdf4ae3d64cf',
    consumer_secret= 'be343ce5215def7540904861dce573d9bc52b3b00b10c9d39223cd50d9d072f1',
    access_token_method='POST')


def get_login():
    return session.get('login')


@rc_auth.tokengetter
def get_rc_oauth_token():
    return get_login()['oauth_token']


def protected(route):
    # in large apps it is probably better to use the Flask-Login extension than
    # this route decorator because this decorator doesn't provide you with
    # 1. user access levels or
    # 2. the helpful abstraction of an "anonymous" user (not yet logged in)
    @wraps(route)
    def wrapper(*args, **kwargs):
        kwargs.update(login=get_login())
        return route(*args, **kwargs) if kwargs['login'] \
            else redirect(url_for('login', next=request.url))
        # redirect includes "next=request.url" so that after logging in the
        # user will be sent to the page they were trying to access
    return wrapper


@app.route('/login')
def login():
    print('View: login')
    if get_login():
        flash('You are already logged in.')
        return redirect(request.referrer or url_for('index'))
    else:
        afterward = request.args.get('next') or request.referrer or None
        print(afterward)
        landing = url_for('oauth_authorized', next=afterward, _external=True)
        print(landing)
        return rc_auth.authorize(callback=landing)


# @app.route('/test')
@app.route('/oauth_authorized')
@rc_auth.authorized_handler
def oauth_authorized(resp):
    print('View: oauth_authorized')
    # print(resp.keys())
    try:
        # make a partial login session here, get the username later if this part works
        # keys into resp are probably different for different oauth providers, unfortunately
        session['login'] = dict(oauth_token=(resp['access_token'], resp['refresh_token']))
    except TypeError as exc:
        flash('The login request was gracefully declined. (TypeError: %s)' % exc)
        return redirect(url_for('index'))
    except KeyError as exc:
        flash('There was a problem with the response dictionary. (KeyError: %s) %s' % (exc, resp))
        return redirect(url_for('index'))
    # now get their username
    me = rc_auth.get('people/me')
    print(me)
    if me.status == 200:
        session['login']['user'] = '{first_name} {last_name}'.format(**me.data)
        session['login']['email'] = me.data['email']
        session['login']['image'] = me.data['image']
    else:
        session['login']['user'] = 'Hacker Schooler'
    flash('You are logged in.')
    print(me.data)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    # the important bit here is to remove the login from the session
    flash('You have logged out.') if session.pop('login', None) \
        else flash('You aren\'t even logged in.')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('home.html', login=get_login())


# @app.route('/matches')
# def show_matches():
#     # TODO: redirect to /coffee
#
#     # Backend: Create list of "users"
#     # Frontend: # List all users
#     users = fetch_users()
#
#     # Backend: stub out a pairing algorithm
#     # Frontend: List current pairings
#     matched_users, unmatched_users = matching.match_users(users)
#
#     # Backend: create algorithm + create tests
#
#     return render_template('test_coffee.html',
#                            users=users,
#                            matched_users=matched_users,
#                            unmatched_users=unmatched_users)


@app.route('/profile')
@protected
def show_profile(login=None):
    print('View: profile')
    return render_template('profile.html', login=login)
    # return "Welcome to the Coffee Matchmaker!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
