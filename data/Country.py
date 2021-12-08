from pony.orm import PrimaryKey, Set, Optional

from data.Base import db
from data.Language import Language


class Country(db.Entity):
    wiki_link = PrimaryKey(str)
    name = Optional(str)
    population = Optional(int)
    Density = Optional(float)
    surface = Optional(float)
    time_zone = Optional(str)
    government = Optional(str)
    languages = Set('Language')
    neighbours = Set('Country', reverse='neighbours')
    capitals = Set('Capital')
    driving_side = Optional(str)
