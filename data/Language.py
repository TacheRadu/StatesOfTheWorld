from peewee import *

from data.Base import BaseModel


class Language(BaseModel):
    language = CharField(primary_key=True)
