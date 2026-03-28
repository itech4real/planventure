"""
Unit tests for PlanVenture API models
"""
import pytest
from app import app, db
from models import User, Trip, Itinerary
from utils import PasswordUtility, JWTUtility


class TestUser:
    """Test User model."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test database."""
        with app.app_context():
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            app.config['TESTING'] = True
            db.create_all()
            yield
            db.session.remove()
            db.drop_all()
    
    def test_create_user(self):
        """Test creating a new user."""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.username == 'testuser'
            assert user.email == 'test@example.com'
    
    def test_password_hashing(self):
        """Test password hashing."""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            password = 'SecurePass123!'
            user.set_password(password)
            
            assert user.password_hash != password
            assert user.check_password(password)
            assert not user.check_password('WrongPassword123!')
    
    def test_user_to_dict(self):
        """Test user to_dict method."""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
            
            user_dict = user.to_dict()
            assert user_dict['username'] == 'testuser'
            assert user_dict['email'] == 'test@example.com'
            assert 'password_hash' not in user_dict


class TestTrip:
    """Test Trip model."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test database."""
        with app.app_context():
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            app.config['TESTING'] = True
            db.create_all()
            yield
            db.session.remove()
            db.drop_all()
    
    def test_create_trip(self):
        """Test creating a trip."""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
            
            trip = Trip(
                user_id=user.id,
                title='Test Trip',
                destination='Paris',
                description='A test trip'
            )
            db.session.add(trip)
            db.session.commit()
            
            assert trip.id is not None
            assert trip.title == 'Test Trip'
            assert trip.user_id == user.id


class TestItinerary:
    """Test Itinerary model."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test database."""
        with app.app_context():
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            app.config['TESTING'] = True
            db.create_all()
            yield
            db.session.remove()
            db.drop_all()
    
    def test_create_itinerary(self):
        """Test creating an itinerary item."""
        with app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('SecurePass123!')
            db.session.add(user)
            db.session.commit()
            
            trip = Trip(
                user_id=user.id,
                title='Test Trip',
                destination='Paris'
            )
            db.session.add(trip)
            db.session.commit()
            
            itinerary = Itinerary(
                trip_id=trip.id,
                day=1,
                title='Visit Eiffel Tower',
                location='Paris'
            )
            db.session.add(itinerary)
            db.session.commit()
            
            assert itinerary.id is not None
            assert itinerary.day == 1
            assert itinerary.title == 'Visit Eiffel Tower'


class TestPasswordUtility:
    """Test password utility functions."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = 'TestPassword123!'
        hashed = PasswordUtility.hash_password(password)
        
        assert hashed != password
        assert PasswordUtility.verify_password(password, hashed)
    
    def test_is_password_strong(self):
        """Test password strength validation."""
        weak_password = 'weak'
        strong_password = 'StrongPass123!'
        
        is_strong, feedback = PasswordUtility.is_password_strong(weak_password)
        assert not is_strong
        assert len(feedback) > 0
        
        is_strong, feedback = PasswordUtility.is_password_strong(strong_password)
        assert is_strong
        assert len(feedback) == 0


class TestJWTUtility:
    """Test JWT utility functions."""
    
    def test_create_tokens(self):
        """Test token creation."""
        user_id = 1
        tokens = JWTUtility.create_tokens(user_id)
        
        assert 'access_token' in tokens
        assert 'refresh_token' in tokens
        assert tokens['token_type'] == 'Bearer'
    
    def test_verify_token(self):
        """Test token verification."""
        user_id = 1
        tokens = JWTUtility.create_tokens(user_id)
        access_token = tokens['access_token']
        
        decoded = JWTUtility.verify_token(access_token)
        assert decoded is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
