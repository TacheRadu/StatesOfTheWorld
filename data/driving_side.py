from pony.orm import Optional, Set

from data.base import db


class DrivingSide(db.Entity):
    driving_side = Optional(str)
    part_of = Set('Country')
