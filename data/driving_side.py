from pony.orm import Optional, Set

from data.base import db


class DrivingSide(db.Entity):
    _table_ = 'DRIVING_SIDES'
    driving_side = Optional(str)
    part_of = Set('Country')
