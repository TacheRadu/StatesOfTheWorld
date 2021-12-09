from pony.orm import PrimaryKey, Optional

from data.base import db


class Capital(db.Entity):
    name = PrimaryKey(str)
    of = Optional('Country')
