#!/usr/bin/python3
"""
Sample minimal flask app
"""


from flask import Flask, render_template
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


@app.route("/python/<text>", strict_slashes=False)
def python_cool(text):
    return f'Python {escape(text.replace("_", " "))}'


@app.route("/python", strict_slashes=False)
@app.route("/python/", strict_slashes=False)
def default_python_cool():
    default = "is cool"
    return f"Python {default}"


@app.route("/number/<int:n>", strict_slashes=False)
def is_number(n):
    """
    displays n if n is an integer

    Returns:
        str: if a n is a number
    """

    if type(n) == int:
        return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def is_number_template(n):
    """
    display a html page

    Returns:
        str: a html page if n is int
    """

    if type(n) == int:
        return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
