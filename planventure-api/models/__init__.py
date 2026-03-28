from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.base import BaseModel
from models.user import User
from models.trip import Trip, Itinerary
from models.trip_share import TripShare
from models.expense import Expense
from models.trip_template import TripTemplate, TemplateItinerary

__all__ = [
    'db', 'BaseModel', 'User', 'Trip', 'Itinerary',
    'TripShare', 'Expense', 'TripTemplate', 'TemplateItinerary'
]
