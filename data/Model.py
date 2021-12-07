from data.Base import db
from data.Country import Country, Neighbours
from data.Language import Language

db.create_tables([Country, Language, Neighbours])