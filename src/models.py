from enum import unique
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# declaring var in the DB 
class Hero(Base):
    __tablename__ = 'hero'
    # /!\ primary key can only be true on one column (like in django)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)