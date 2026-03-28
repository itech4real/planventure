#!/usr/bin/env python
"""
Seed database with sample data
Usage: python seed_db.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app import app, db
from models import User, Trip

def seed_database():
    """Seed the database with sample data."""
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database with sample data...")
        
        # Create sample users
        user1 = User(username='john_doe', email='john@example.com')
        user1.set_password('password123')
        
        user2 = User(username='jane_smith', email='jane@example.com')
        user2.set_password('password456')
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        print(f"✓ Created {User.query.count()} users")
        
        # Create sample trips
        trip1 = Trip(
            user_id=user1.id,
            title='Summer Vacation in Europe',
            description='Explore the beautiful cities of Europe',
            destination='Paris, France',
            start_date=datetime.now() + timedelta(days=30),
            end_date=datetime.now() + timedelta(days=45)
        )
        
        trip2 = Trip(
            user_id=user1.id,
            title='Beach Getaway',
            description='Relax at a tropical beach',
            destination='Bali, Indonesia',
            start_date=datetime.now() + timedelta(days=60),
            end_date=datetime.now() + timedelta(days=75)
        )
        
        trip3 = Trip(
            user_id=user2.id,
            title='Mountain Hiking Adventure',
            description='Trek through mountain ranges',
            destination='Swiss Alps',
            start_date=datetime.now() + timedelta(days=20),
            end_date=datetime.now() + timedelta(days=35)
        )
        
        db.session.add_all([trip1, trip2, trip3])
        db.session.commit()
        
        print(f"✓ Created {Trip.query.count()} trips")
        print("✓ Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
