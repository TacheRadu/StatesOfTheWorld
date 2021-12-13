from pony.orm import Required, Set

from data.base import db


class Language(db.Entity):
    """Class corresponding to the DB table for languages."""
    _table_ = 'languages'
    language = Required(str)
    part_of = Set('LanguageCategory')
