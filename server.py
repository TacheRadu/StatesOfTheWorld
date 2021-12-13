from flask import Flask
from controllers.top import *
from controllers.countries import *

app = Flask(__name__)


@app.route('/top/<int:top_count>/<criteria>')
def top(top_count, criteria):
    if criteria == 'population':
        return by_population(top_count)
    elif criteria == 'density':
        return by_density(top_count)
    elif criteria == 'surface':
        return by_area(top_count)
    elif criteria == 'number-of-neighbours':
        return by_number_of_neighbours(top_count)


@app.route('/countries/<criteria>/<value>')
def countries(criteria, value):
    if criteria == 'language':
        return countries_by_language(value)
