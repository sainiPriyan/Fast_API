from .database import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index = True)
    name = Column(String)
    age = Column(Integer)
    phone = Column(Integer, unique=True, index=True)