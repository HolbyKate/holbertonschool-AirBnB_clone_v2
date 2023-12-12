#!/usr/bin/python3
"""
Simple Flask web application with routes to display 'Hello HBNB', 'HBNB',
handle 'C' and 'Python' routes, and display numbers
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)

@app.teardown_appcontext
def teardown_appcontext(self):
    """Closes storage"""
    storage.close()

@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays HTML page with list of states"""
    states = storage.all('State')
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
