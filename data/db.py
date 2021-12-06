from typing import Union, Any
from sqlalchemy import create_engine
from sqlalchemy.engine.mock import MockConnection
import data.Country
import data.Language
from data.base import Base

engine: Union[MockConnection, Any] = create_engine('mysql+pymysql://root:@localhost:3306/states_of_the_world')
Base.metadata.create_all(engine)
