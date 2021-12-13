from pony.orm import PrimaryKey, Set, Optional

from data.base import db


class LanguageCategory(db.Entity):
    _table_ = 'LANGUAGE_CATEGORIES'
    category = PrimaryKey(str)
    of = Optional('Country')
    languages = Set('Language', table='languages_in_category')
