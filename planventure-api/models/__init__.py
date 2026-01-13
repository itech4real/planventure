from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.base import BaseModel
from models.user import User
from models.trip import Trip, Itinerary

__all__ = ['db', 'BaseModel', 'User', 'Trip', 'Itinerary']
