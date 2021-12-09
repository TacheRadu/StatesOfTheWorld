from pony.orm import PrimaryKey, Set

from data.base import db


class Language(db.Entity):
    language = PrimaryKey(str)
    part_of = Set('LanguageCategory')
