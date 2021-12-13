from flask import Flask
from controllers.top import *

app = Flask(__name__)


@app.route('/top/<int:top_count>/<criteria>')
def top(top_count, criteria):
    if criteria == 'population':
        return by_population(top_count)
