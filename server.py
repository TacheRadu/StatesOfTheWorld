from flask import Flask, Response
from controllers.top import *
from controllers.countries import *

app = Flask(__name__)


@app.route('/top/<int:top_count>/<criteria>')
def top(top_count, criteria):
    if criteria == 'population':
        return Response(by_population(top_count), mimetype='application/json')
    elif criteria == 'density':
        return Response(by_density(top_count), mimetype='application/json')
    elif criteria == 'surface':
        return Response(by_area(top_count), mimetype='application/json')
    elif criteria == 'number-of-neighbours':
        return Response(by_number_of_neighbours(top_count), mimetype='application/json')


@app.route('/countries/<criteria>/<value>')
def countries(criteria, value):
    if criteria == 'language':
        return Response(countries_by_language(value), mimetype='application/json')
    elif criteria == 'time-zone':
        return Response(countries_by_time_zone(value), mimetype='application/json')
    elif criteria == 'government':
        return Response(countries_by_government(value), mimetype='application/json')
    elif criteria == 'driving-side':
        return Response(countries_by_driving_side(value), mimetype='application/json')


@app.route('/country/<country_name>')
def country(country_name):
    return Response(country_info(country_name), mimetype='application/json')
