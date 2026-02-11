"""
Expense tracking model for trips
"""
from models import db
from models.base import BaseModel


class Expense(BaseModel):
    """Model for tracking expenses in trips."""
    __tablename__ = 'expenses'
    
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id', ondelete='CASCADE'), nullable=False)
    paid_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    category = db.Column(db.String(50), nullable=False)  # 'accommodation', 'food', 'transport', 'activity', 'other'
    description = db.Column(db.String(500))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD', nullable=False)
    date = db.Column(db.DateTime)
    
    # Relationships
    trip = db.relationship('Trip', backref='expenses', lazy=True)
    paid_by_user = db.relationship('User', backref='expenses', lazy=True)
    
    def __repr__(self):
        return f'<Expense {self.category} ${self.amount}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'trip_id': self.trip_id,
            'paid_by_user_id': self.paid_by_user_id,
            'category': self.category,
            'description': self.description,
            'amount': self.amount,
            'currency': self.currency,
            'date': self.date.isoformat() if self.date else None,
            'paid_by_user': self.paid_by_user.to_dict() if self.paid_by_user else None
        })
        return data
