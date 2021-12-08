from pony.orm import PrimaryKey, Set

from data.Base import db


class Language(db.Entity):
    language = PrimaryKey(str)
    spoken_in = Set('Country')
