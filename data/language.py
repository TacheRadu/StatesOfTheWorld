from pony.orm import PrimaryKey, Set

from data.base import db


class Language(db.Entity):
    """Class corresponding to the DB table for languages."""
    _table_ = 'LANGUAGES'
    language = PrimaryKey(str)
    part_of = Set('LanguageCategory')
