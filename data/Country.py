from peewee import *

from data.Language import Language
from data.Base import BaseModel


class Country(BaseModel):
    name = CharField(primary_key=True)
    capital = CharField()
    population = IntegerField()
    Density = FloatField()
    surface = FloatField()
    time_zone = CharField()
    government = CharField()
    languages = ManyToManyField(Language)
    driving_side = CharField()


class Neighbours(BaseModel):
    first_country = ForeignKeyField(Country, backref='neighbours')
    second_country = ForeignKeyField(Country, backref='neighbours')
