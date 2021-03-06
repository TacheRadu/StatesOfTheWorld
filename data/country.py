from pony.orm import PrimaryKey, Set, Optional

from data.base import db


class Country(db.Entity):
    """Class corresponding to the DB table for countries."""
    _table_ = 'countries'
    wiki_link = PrimaryKey(str)
    name = Optional(str)
    population = Optional(int)
    density = Optional(float)
    surface = Optional(float)
    time_zone = Optional(str)
    government = Optional(str)
    language_categories = Set('LanguageCategory')
    neighbours = Set('Country', reverse='neighbours')
    capitals = Set('Capital')
    driving_side = Optional('DrivingSide')
