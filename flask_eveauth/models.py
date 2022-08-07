from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Model(Base):
    id = Column(Integer, primary_key=True)


class Role(Model):
    __tablename__ = 'role'


class Session(Model):
    __tablename__ = 'session'


class Token(Model):
    __tablename__ = 'token'


class User(Model):
    __tablename__ = 'user'
