"""
Trip sharing model for collaboration
"""
from models import db
from models.base import BaseModel


class TripShare(BaseModel):
    """Model for sharing trips with other users."""
    __tablename__ = 'trip_shares'
    
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id', ondelete='CASCADE'), nullable=False)
    shared_with_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    permission = db.Column(db.String(20), default='view', nullable=False)  # 'view', 'edit', 'admin'
    
    # Relationships
    trip = db.relationship('Trip', backref='shares', lazy=True)
    shared_with_user = db.relationship('User', backref='shared_trips', lazy=True)
    
    __table_args__ = (db.UniqueConstraint('trip_id', 'shared_with_user_id', name='unique_trip_share'),)
    
    def __repr__(self):
        return f'<TripShare trip_id={self.trip_id} user_id={self.shared_with_user_id}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        data = super().to_dict()
        data.update({
            'trip_id': self.trip_id,
            'shared_with_user_id': self.shared_with_user_id,
            'permission': self.permission,
            'shared_with_user': self.shared_with_user.to_dict() if self.shared_with_user else None
        })
        return data
