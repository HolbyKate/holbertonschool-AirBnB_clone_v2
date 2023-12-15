#!/usr/bin/python3
"""
Script that starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from os import environ

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(exception):
    storage.close()


@app.route('/hbnb_filters')
def hbnb_filters():
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    cities = storage.all(City).values()

    states = sorted(states, key=lambda state: state.name)
    cities = sorted(cities, key=lambda city: city.name)
    amenities = sorted(amenities, key=lambda amenity: amenity.name)

    return render_template(
        '10-hbnb_filters.html',
        states=states,
        cities=cities,
        amenities=amenities
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)