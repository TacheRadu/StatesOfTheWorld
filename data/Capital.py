from pony.orm import PrimaryKey, Optional

from data.Base import db


class Capital(db.Entity):
    name = PrimaryKey(str)
    of = Optional('Country')
