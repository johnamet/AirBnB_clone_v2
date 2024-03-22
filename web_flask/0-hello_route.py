#!/usr/bin/python3
"""
Sample minimal flask app
"""


from flask import Flask


app = Flask(__name__)
app.config['SERVER_NAME'] = '0.0.0.0:5000'


@app.route("/", strict_slashes=False)
def hello_route():
    """
    Return hello
    """

    return "Hello HBNB!"


if __name__ == "__main__":
    app.run()
