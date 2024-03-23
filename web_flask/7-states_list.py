#!/usr/bin/python3
"""
The script displays a list of states
"""


from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    states = storage.all(State)
    states_list = [state for _, state in states.items()]
    return render_template('7-states_list.html', states=states_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
