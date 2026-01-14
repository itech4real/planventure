"""
Trip template model for reusable trip plans
"""
from models import db
from models.base import BaseModel


class TripTemplate(BaseModel):
    """Model for pre-made trip templates."""
    __tablename__ = 'trip_templates'
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    destination = db.Column(db.String(200), nullable=False)
    duration_days = db.Column(db.Integer, default=7, nullable=False)
    category = db.Column(db.String(50))  # 'adventure', 'relaxation', 'cultural', 'business', 'family'
    difficulty = db.Column(db.String(20), default='medium')  # 'easy', 'medium', 'hard'
    estimated_budget = db.Column(db.Float)
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    
    # Relationships
    created_by_user = db.relationship('User', backref='templates', lazy=True)
    template_items = db.relationship('TemplateItinerary', backref='template', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<TripTemplate {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'destination': self.destination,
            'duration_days': self.duration_days,
            'category': self.category,
            'difficulty': self.difficulty,
            'estimated_budget': self.estimated_budget,
            'is_public': self.is_public,
            'created_by_user_id': self.created_by_user_id,
            'items': [item.to_dict() for item in self.template_items]
        })
        return data


class TemplateItinerary(BaseModel):
    """Model for itinerary items in a trip template."""
    __tablename__ = 'template_itineraries'
    
    template_id = db.Column(db.Integer, db.ForeignKey('trip_templates.id', ondelete='CASCADE'), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    activity_type = db.Column(db.String(50))  # 'sightseeing', 'hiking', 'food', 'shopping', 'rest'
    
    def __repr__(self):
        return f'<TemplateItinerary {self.title}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'template_id': self.template_id,
            'day': self.day,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'activity_type': self.activity_type
        })
        return data
