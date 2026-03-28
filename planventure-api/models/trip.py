from models import db
from models.base import BaseModel

class Trip(BaseModel):
    """Trip model for user travel plans."""
    __tablename__ = 'trips'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    destination = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    
    # Relationships
    itineraries = db.relationship('Itinerary', backref='trip', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Trip {self.title}>'
    
    def to_dict(self):
        """Convert trip to dictionary."""
        data = super().to_dict()
        data.update({
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'destination': self.destination,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'itineraries': [itinerary.to_dict() for itinerary in self.itineraries]
        })
        return data


class Itinerary(BaseModel):
    """Itinerary model for trip activities and schedules."""
    __tablename__ = 'itineraries'
    
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False, index=True)
    day = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Itinerary {self.title} - Day {self.day}>'
    
    def to_dict(self):
        """Convert itinerary to dictionary."""
        data = super().to_dict()
        data.update({
            'id': self.id,
            'trip_id': self.trip_id,
            'day': self.day,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        })
        return data
