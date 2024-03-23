#!/usr/bin/python3
"""
List all cities by states
"""

from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    states = storage.all(State)
    states_list = [state for _, state in states.items()]
    return render_template('8-cities_by_states.html', states=states_list)


@app.teardown_appcontext
def close_db(exception=None):
    """
    After each request remove the current SQLAlchemy Session:
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

