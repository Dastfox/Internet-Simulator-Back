from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

# declaring var in the DB 
class Hero(Base):
    __tablename__ = 'Hero'
    # /!\ primary key can only be true on one column (like in django)
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique = True, index=True)