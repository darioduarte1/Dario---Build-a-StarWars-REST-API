import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=True)
    first_name = Column(String(250), nullable=True)
    last_name = Column(String(250), nullable=True)
    email = Column(String(250), nullable=True)
    password = Column(String(250), nullable=True)
    favorite = relationship("Favorites", backref="user")

    def __repr__(self):
        return '<User %r>' % self.email
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)
    race = Column(String(250), nullable=True)
    height = Column(String(250), nullable=True)
    eyes_color = Column(String(250), nullable=True)

    def __repr__(self):
        return '<Characters %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "race": self.race,
            "height": self.height,
            "eyesColor": self.eyes_color,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)
    local = Column(String(250), nullable=True)
    dimension = Column(String(250), nullable=True)
    color = Column(String(250), nullable=True)
    favorite = relationship("Favorites", backref="planets")

    def __repr__(self):
        return '<Planets %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "local": self.local,
            "dimension": self.dimension,
            "color": self.color,
            # do not serialize the password, its a security breach
        }

class Spaceships(db.Model):
    __tablename__ = 'spaceships'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)
    color = Column(String(250), nullable=True)
    guns = Column(String(250), nullable=True)
    velocity = Column(String(250), nullable=True)
    favorite = relationship("Favorites", backref="spaceships")

    def __repr__(self):
        return '<Spaceships %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "guns": self.guns,
            "velocity": self.velocity,
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_fk = Column(Integer, ForeignKey("user.id"))
    characters_fk = Column(Integer, ForeignKey("characters.id"))
    planet_fk = Column(Integer, ForeignKey("planets.id"))
    spaceships_fk = Column(Integer, ForeignKey("spaceships.id"))

    def __repr__(self):
        return '<Favorites %r>' % self.id
    def serialize(self):
        return {
            "id": self.id,
            "userFK": self.user_fk,
            "charactersFK": self.characters_fk,
            "PlanetFK": self.planet_fk,
            "spaceshipsFK": self.spaceships_fk,
            # do not serialize the password, its a security breach
        }
    


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
