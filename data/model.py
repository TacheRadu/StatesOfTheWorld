from data.base import db
from data.country import Country
from data.language import Language
from data.capital import Capital
from data.language_category import LanguageCategory

db.bind(provider='mysql', host='localhost', user='root', password='', database='states_of_the_world')
db.generate_mapping(create_tables=True)
