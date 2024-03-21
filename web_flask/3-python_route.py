#!/usr/bin/python3
# Sample minimal flask app
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hello_hbnb():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_is_fun(text):
    return f'C {escape(text.replace("_", " "))}'


@app.route("/python/<text>")
def python_cool(text):
    return f'Python {escape(text.replace("_", " "))}'


@app.route("/python")
@app.route("/python/")
def default_python_cool():
    default = "is cool"
    return f"Python {default}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
