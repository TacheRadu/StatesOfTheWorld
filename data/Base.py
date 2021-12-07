from peewee import *

db = MySQLDatabase('states_of_the_world', user='root')


class BaseModel(Model):
    class Meta:
        database = db
