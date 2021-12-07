from data.Base import db
from data.Country import Country
from data.Language import Language

db.create_tables([Country, Language])