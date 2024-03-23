#!/usr/bin/python3
"""
List all cities by states
"""

from flask import Flask, render_template
from models import storage, State, Amenity

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def states_list():
    """
    List all states
    """
    states = storage.all(State).values()
    amenites = storage.all(Amenity).values()
    data = {
        'states': states,
        'amenities': amenites
    }
    return render_template('10-hbnb_filters.html', data=data)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """
    Get state by id
    """
    states = storage.all(State)
    state = [state for state in states.values() if id == state.id]
    if state:
        state = state[0]
    else:
        state = None
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def close_db(exception=None):
    """
    After each request remove the current SQLAlchemy Session:
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
