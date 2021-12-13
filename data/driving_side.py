from pony.orm import Optional, Set

from data.base import db


class DrivingSide(db.Entity):
    """Class corresponding to the DB table for driving sides."""
    _table_ = 'driving_sides'
    driving_side = Optional(str)
    part_of = Set('Country')
