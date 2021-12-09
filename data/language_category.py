from pony.orm import PrimaryKey, Set, Optional

from data.base import db


class LanguageCategory(db.Entity):
    category = PrimaryKey(str)
    of = Optional('Country')
    languages = Set('Language')
