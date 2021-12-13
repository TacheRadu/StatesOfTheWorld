from pony.orm import PrimaryKey, Optional

from data.base import db


class Capital(db.Entity):
    """Class corresponding to the DB table for capitals."""
    _table_ = 'CAPITALS'
    name = PrimaryKey(str)
    of = Optional('Country')
