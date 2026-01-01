from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String)
    age = Column(Integer)
    phone = Column(Integer, unique=True, index=True)

    login_id = Column(Integer, ForeignKey('login_details.id'))

    login_details = relationship('LoginDetails', back_populates='user')

class LoginDetails(Base):
    __tablename__ = 'login_details'

    id = Column(Integer, primary_key=True, index = True)
    name = Column(String)
    password = Column(String)
    email = Column(String,  unique=True)

    user = relationship('User', back_populates='login_details' )