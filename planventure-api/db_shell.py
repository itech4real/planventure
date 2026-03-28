#!/usr/bin/env python
"""
Interactive database shell
Provides a Python shell with app context and models loaded
Usage: python db_shell.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app import app, db
from models import User, Trip

def main():
    """Start interactive Python shell with app context."""
    import code
    
    with app.app_context():
        # Create banner
        banner = """
PlanVenture Database Shell
==========================
Available objects:
  - app: Flask application
  - db: SQLAlchemy database instance
  - User: User model
  - Trip: Trip model

Examples:
  # Create tables
  >>> db.create_all()
  
  # Query all users
  >>> User.query.all()
  
  # Create a user
  >>> user = User(username='test', email='test@example.com')
  >>> user.set_password('password123')
  >>> db.session.add(user)
  >>> db.session.commit()
  
  # Query specific user
  >>> User.query.filter_by(username='test').first()
"""
        
        # Create interactive console
        local_vars = {
            'app': app,
            'db': db,
            'User': User,
            'Trip': Trip,
        }
        
        console = code.InteractiveConsole(local_vars)
        console.interact(banner=banner)

if __name__ == '__main__':
    main()
