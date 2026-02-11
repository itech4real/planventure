"""
Integration tests for PlanVenture API endpoints
"""
import json
import pytest
from app import app, db
from models import User


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def auth_user(client):
    """Create and authenticate a test user."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('TestPassword123!')
        db.session.add(user)
        db.session.commit()
        
        # Register and login
        response = client.post('/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        })
        
        if response.status_code == 409:  # User already exists
            login_response = client.post('/auth/login', json={
                'email': 'test@example.com',
                'password': 'TestPassword123!'
            })
            return login_response.get_json()['access_token']
        
        return response.get_json()['access_token']


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test /health endpoint."""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['username'] == 'newuser'
    
    def test_register_duplicate_user(self, client, auth_user):
        """Test registration with duplicate email."""
        response = client.post('/auth/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123!'
        })
        
        assert response.status_code == 409
    
    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        response = client.post('/auth/register', json={
            'username': 'weakuser',
            'email': 'weak@example.com',
            'password': 'weak'
        })
        
        assert response.status_code == 400
    
    def test_login_success(self, client, auth_user):
        """Test successful login."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
    
    def test_login_invalid_credentials(self, client, auth_user):
        """Test login with invalid credentials."""
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'WrongPassword123!'
        })
        
        assert response.status_code == 401
    
    def test_refresh_token(self, client, auth_user):
        """Test token refresh."""
        # First login
        login_response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        })
        
        refresh_token = login_response.get_json()['refresh_token']
        
        # Use refresh token
        headers = {'Authorization': f'Bearer {refresh_token}'}
        response = client.post('/auth/refresh', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data


class TestProfileEndpoint:
    """Test profile endpoint."""
    
    def test_get_profile(self, client, auth_user):
        """Test getting user profile."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        response = client.get('/profile', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'username' in data
        assert 'email' in data
    
    def test_get_profile_unauthorized(self, client):
        """Test getting profile without token."""
        response = client.get('/profile')
        
        assert response.status_code == 401


class TestTripsEndpoints:
    """Test trips CRUD endpoints."""
    
    def test_get_trips(self, client, auth_user):
        """Test getting all trips."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        response = client.get('/trips', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_create_trip(self, client, auth_user):
        """Test creating a trip."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        response = client.post('/trips', headers=headers, json={
            'title': 'New Trip',
            'destination': 'Tokyo',
            'description': 'A trip to Tokyo'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'New Trip'
        assert data['destination'] == 'Tokyo'
    
    def test_get_trip(self, client, auth_user):
        """Test getting a specific trip."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        
        # Create a trip
        create_response = client.post('/trips', headers=headers, json={
            'title': 'New Trip',
            'destination': 'Tokyo'
        })
        trip_id = create_response.get_json()['id']
        
        # Get the trip
        response = client.get(f'/trips/{trip_id}', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == trip_id
    
    def test_update_trip(self, client, auth_user):
        """Test updating a trip."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        
        # Create a trip
        create_response = client.post('/trips', headers=headers, json={
            'title': 'Old Title',
            'destination': 'Tokyo'
        })
        trip_id = create_response.get_json()['id']
        
        # Update the trip
        response = client.put(f'/trips/{trip_id}', headers=headers, json={
            'title': 'New Title',
            'destination': 'Osaka'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['title'] == 'New Title'
        assert data['destination'] == 'Osaka'
    
    def test_delete_trip(self, client, auth_user):
        """Test deleting a trip."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        
        # Create a trip
        create_response = client.post('/trips', headers=headers, json={
            'title': 'New Trip',
            'destination': 'Tokyo'
        })
        trip_id = create_response.get_json()['id']
        
        # Delete the trip
        response = client.delete(f'/trips/{trip_id}', headers=headers)
        
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f'/trips/{trip_id}', headers=headers)
        assert get_response.status_code == 404


class TestItineraryEndpoints:
    """Test itinerary endpoints."""
    
    def test_get_itinerary(self, client, auth_user):
        """Test getting itinerary items."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        
        # Create a trip
        create_trip = client.post('/trips', headers=headers, json={
            'title': 'New Trip',
            'destination': 'Tokyo'
        })
        trip_id = create_trip.get_json()['id']
        
        # Get itinerary
        response = client.get(f'/trips/{trip_id}/itinerary', headers=headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_create_itinerary_item(self, client, auth_user):
        """Test creating an itinerary item."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        
        # Create a trip
        create_trip = client.post('/trips', headers=headers, json={
            'title': 'New Trip',
            'destination': 'Tokyo'
        })
        trip_id = create_trip.get_json()['id']
        
        # Create itinerary item
        response = client.post(f'/trips/{trip_id}/itinerary', headers=headers, json={
            'day': 1,
            'title': 'Visit Temple',
            'location': 'Tokyo',
            'notes': 'Historic temple'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['day'] == 1
        assert data['title'] == 'Visit Temple'
    
    def test_update_itinerary_item(self, client, auth_user):
        """Test updating an itinerary item."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        
        # Create trip and itinerary
        create_trip = client.post('/trips', headers=headers, json={
            'title': 'New Trip',
            'destination': 'Tokyo'
        })
        trip_id = create_trip.get_json()['id']
        
        create_item = client.post(f'/trips/{trip_id}/itinerary', headers=headers, json={
            'day': 1,
            'title': 'Visit Temple',
            'location': 'Tokyo'
        })
        item_id = create_item.get_json()['id']
        
        # Update item
        response = client.put(f'/trips/{trip_id}/itinerary/{item_id}', headers=headers, json={
            'day': 2,
            'title': 'Visit Shrine',
            'location': 'Tokyo'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['day'] == 2
        assert data['title'] == 'Visit Shrine'
    
    def test_delete_itinerary_item(self, client, auth_user):
        """Test deleting an itinerary item."""
        headers = {'Authorization': f'Bearer {auth_user}'}
        
        # Create trip and itinerary
        create_trip = client.post('/trips', headers=headers, json={
            'title': 'New Trip',
            'destination': 'Tokyo'
        })
        trip_id = create_trip.get_json()['id']
        
        create_item = client.post(f'/trips/{trip_id}/itinerary', headers=headers, json={
            'day': 1,
            'title': 'Visit Temple',
            'location': 'Tokyo'
        })
        item_id = create_item.get_json()['id']
        
        # Delete item
        response = client.delete(f'/trips/{trip_id}/itinerary/{item_id}', headers=headers)
        
        assert response.status_code == 204


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
