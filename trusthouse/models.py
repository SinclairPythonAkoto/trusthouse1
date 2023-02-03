from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from trusthouse.extensions import Base

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    door_num = Column(String(35), nullable=False)
    street = Column(String(60), nullable=False)
    location = Column(String(50), nullable=False)
    postcode = Column(String(10), nullable=False)
    geo_map = relationship('Maps', backref='location', uselist=False)
    reviews = relationship('Reviews', backref='address')
    buisnesses = relationship('Business', backref='place')
    incident = relationship('Incident', backref='area')

class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)
    type = Column(String(20), nullable=False)
    date = Column(DateTime, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))

class Maps(Base):
    __tablename__ = 'maps'
    id = Column(Integer, primary_key=True)
    lon = Column(String(15), nullable=False)
    lat = Column(String(15), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))

class Business(Base):
    __tablename__ = 'business'
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    category = Column(String(15), nullable=False)
    contact = Column(String(50), nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))

class Incident(Base):
    __tablename__ = 'incident'
    id = Column(Integer, primary_key=True)
    category = Column(String(15), nullable=False)
    description = Column(String(40), nullable=False)
    date = Column(DateTime, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))
