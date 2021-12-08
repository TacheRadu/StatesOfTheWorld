from peewee import *

from data.Language import Language
from data.Base import BaseModel


class Country(BaseModel):
    wiki_link = CharField(primary_key=True)
    name = CharField()
    capital = CharField()
    population = IntegerField()
    Density = FloatField()
    surface = FloatField()
    time_zone = CharField()
    government = CharField()
    languages = ManyToManyField(Language)
    driving_side = CharField()

    def save_neighbours(self):
        for neighbour in self.neighbours:
            Neighbours.get_or_create(first_country=self, second_country=neighbour)
            Neighbours.get_or_create(first_country=neighbour, second_country=self)

    def get_neighbours(self) -> list:
        Neighbour = Country.alias()
        return Country.select(Neighbour)\
            .join(Neighbours, on=Neighbours.first_country)\
            .join(Neighbour, on=Neighbours.second_country)\
            .where(Neighbours.first_country == self)


class Neighbours(BaseModel):
    first_country = ForeignKeyField(Country, backref='neighbours')
    second_country = ForeignKeyField(Country, backref='neighbours')
