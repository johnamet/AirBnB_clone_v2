#!/usr/bin/python3
"""
List all cities by states
"""

from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states_list():
    """
    List all states
    """
    states = storage.all(State)
    states_list = [state for _, state in states.items()]
    return render_template('7-states_list.html', states=states_list)


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
