# user endpoint
# database

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    # TODO: redirect to coffee
    # List all users
    # List current pairings
    return render_template('test_coffee.html')

@app.route('/coffee')
def coffee():
    return "Welcome to the Coffee Matchmaker!"

if __name__=='__main__':
    app.run(debug=True)
