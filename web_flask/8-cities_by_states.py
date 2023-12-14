#!/usr/bin/python3
"""
Simple Flask web application with routes to display 'Hello HBNB', 'HBNB',
handle 'C' and 'Python' routes, and display numbers
"""

from flask import Flask, redirect, render_template, request
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/', strict_slashes=False)
def hello_HBNB():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def HBNB():
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    text = text.replace('_', ' ')
    return 'C {}'.format(text)


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', strict_slashes=False)
def python_route(text='is cool'):
    text = text.replace('_', ' ')
    return 'Python {}'.format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    return render_template('6-number_odd_or_even.html', n=n)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.route("/states_list", strict_slashes=False)
def display_html():
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)

    return render_template("7-states_list.html", states=sorted_states)


@app.route("/add_state", methods=['POST'])
def add_state():
    if request.method == 'POST':
        new_state_name = request.json.get('name')

        new_state = State(name=new_state_name)
        storage.new(new_state)
        storage.save()

    return redirect("/states_list")


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display a HTML page with a list of all State objects in DBStorage."""
    states = storage.all(State)
    cities = storage.all(City)

    return render_template("8-cities_by_states.html",
                           cities=cities,
                           states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
