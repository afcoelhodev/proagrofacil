# Generate the classes that will build the table and objects inside them

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Users_db(Base):
    __tablename__ = 'Users'

    username = Column(String(length=50), primary_key=True)
    password = Column(String(length=250), nullable=False)

    def __repr__(self):
        return "<User %r>" %self.username

class Agro_db(Base):
    __tablename__ = 'Agro_manager'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=180))
    cpf = Column(String(length=11))
    email = Column(String(length=180))
    local_LAT = Column(String(length=10))
    local_LON = Column(String(length=10))
    lavoura = Column(String(length=180))
    colheita = Column(String(length=10))
    causa = Column(String(length=180))

    def __repr__(self):
        return "<Lavoura manage by %r>" %self.name