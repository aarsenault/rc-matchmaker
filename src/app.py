# user endpoint
# database

import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from models.models import db

# import matching
# from users import fetch_users
# from models import User
from models import matching
from models.users import fetch_users
# from src.models.models import User

app = Flask(__name__)

# APP_SETTINGS picked up from autoenv and .env file
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Sanity Checker for env variables
print( 'Environment configuratino is: {}'.format( os.environ['APP_SETTINGS']) )


@app.route('/')
def index():
    return  render_template('home.html')


@app.route('/matches')
def show_matches():
    # TODO: redirect to /coffee

    # Backend: Create list of "users"
    # Frontend: # List all users
    users = fetch_users()

    # Backend: stub out a pairing algorithm
    # Frontend: List current pairings
    matched_users, unmatched_users = matching.match_users(users)

    # Backend: create algorithm + create tests

    return render_template('test_coffee.html',
                           users=users,
                           matched_users=matched_users,
                           unmatched_users=unmatched_users)


@app.route('/profile')
def show_profile():
    return render_template('profile.html')
    # return "Welcome to the Coffee Matchmaker!"


if __name__ == '__main__':
    app.run(debug=True)
