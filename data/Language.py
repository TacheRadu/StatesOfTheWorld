from data.base import Base
from sqlalchemy import Column, String


class Language(Base):
    __tablename__ = 'LANGUAGES'
    language = Column(String(255), primary_key=True)
