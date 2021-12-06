from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from data.base import Base


class Country(Base):
    __tablename__ = 'COUNTRIES'
    name = Column(String(255), primary_key=True)
    capital = Column(String(255))
    population = Column(Integer)
    density = Column(String(255))
    surface = Column(Float)
    time_zone = Column(String(255))
    government = Column(String(255))
    neighbours = relationship('COUNTRIES', back_populates='neighbours')
    languages = relationship('LANGUAGES')
    driving_side = Column(String(255))
