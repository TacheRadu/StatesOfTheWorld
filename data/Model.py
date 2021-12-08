from data.Base import db
from data.Country import Country
from data.Language import Language

db.bind(provider='mysql', host='localhost', user='root', password='', database='states_of_the_world')
db.generate_mapping(create_tables=True)
