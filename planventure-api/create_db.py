#!/usr/bin/env python
"""
Database initialization script
Initializes the SQLAlchemy database tables
Usage: python create_db.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent))

from app import app, db
from models import User, Trip

def create_tables():
    """Create all database tables."""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        print(f"✓ Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")

def drop_tables():
    """Drop all database tables."""
    with app.app_context():
        print("Dropping all database tables...")
        db.drop_all()
        print("✓ All database tables dropped!")

def reset_db():
    """Reset database (drop and recreate tables)."""
    with app.app_context():
        print("Resetting database...")
        db.drop_all()
        print("✓ Dropped all tables")
        db.create_all()
        print("✓ Created all tables")
        print("✓ Database reset successfully!")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Database management utility')
    parser.add_argument(
        'action',
        choices=['create', 'drop', 'reset'],
        help='Action to perform on the database'
    )
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_tables()
    elif args.action == 'drop':
        confirm = input("Are you sure you want to drop all tables? (yes/no): ")
        if confirm.lower() == 'yes':
            drop_tables()
        else:
            print("Cancelled.")
    elif args.action == 'reset':
        confirm = input("Are you sure you want to reset the database? (yes/no): ")
        if confirm.lower() == 'yes':
            reset_db()
        else:
            print("Cancelled.")
