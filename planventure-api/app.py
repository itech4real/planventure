from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables
load_dotenv()

# Import models
from models import db, User, Trip, Itinerary

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///planventure.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# Routes - Health & Info
@app.route('/')
def home():
    return jsonify({"message": "Welcome to PlanVenture API", "version": "1.0.0"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/version', methods=['GET'])
def version():
    return jsonify({'version': '1.0.0'}), 200

# Routes - Authentication
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 409
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully", "user": user.to_dict()}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200

# Routes - Trips
@app.route('/trips', methods=['GET'])
@jwt_required()
def get_trips():
    user_id = get_jwt_identity()
    trips = Trip.query.filter_by(user_id=user_id).all()
    return jsonify([trip.to_dict() for trip in trips]), 200

@app.route('/trips', methods=['POST'])
@jwt_required()
def create_trip():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('destination'):
        return jsonify({"error": "Missing required fields"}), 400
    
    trip = Trip(
        user_id=user_id,
        title=data['title'],
        description=data.get('description'),
        destination=data['destination'],
        start_date=data.get('start_date'),
        end_date=data.get('end_date')
    )
    
    db.session.add(trip)
    db.session.commit()
    
    return jsonify({"message": "Trip created successfully", "trip": trip.to_dict()}), 201

@app.route('/trips/<int:trip_id>', methods=['GET'])
@jwt_required()
def get_trip(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    return jsonify(trip.to_dict()), 200

@app.route('/trips/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        trip.title = data['title']
    if 'description' in data:
        trip.description = data['description']
    if 'destination' in data:
        trip.destination = data['destination']
    if 'start_date' in data:
        trip.start_date = data['start_date']
    if 'end_date' in data:
        trip.end_date = data['end_date']
    
    db.session.commit()
    
    return jsonify({"message": "Trip updated successfully", "trip": trip.to_dict()}), 200

@app.route('/trips/<int:trip_id>', methods=['DELETE'])
@jwt_required()
def delete_trip(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    db.session.delete(trip)
    db.session.commit()
    
    return jsonify({"message": "Trip deleted successfully"}), 200

# Routes - Itinerary
@app.route('/trips/<int:trip_id>/itinerary', methods=['GET'])
@jwt_required()
def get_itinerary(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    itineraries = Itinerary.query.filter_by(trip_id=trip_id).order_by(Itinerary.day).all()
    return jsonify([item.to_dict() for item in itineraries]), 200

@app.route('/trips/<int:trip_id>/itinerary', methods=['POST'])
@jwt_required()
def create_itinerary_item(trip_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    data = request.get_json()
    
    if not data or not data.get('day') or not data.get('title'):
        return jsonify({"error": "Missing required fields (day, title)"}), 400
    
    itinerary = Itinerary(
        trip_id=trip_id,
        day=data['day'],
        title=data['title'],
        description=data.get('description'),
        location=data.get('location'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        start_time=data.get('start_time'),
        end_time=data.get('end_time')
    )
    
    db.session.add(itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary item created successfully", "itinerary": itinerary.to_dict()}), 201

@app.route('/trips/<int:trip_id>/itinerary/<int:item_id>', methods=['GET'])
@jwt_required()
def get_itinerary_item(trip_id, item_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    itinerary = Itinerary.query.filter_by(id=item_id, trip_id=trip_id).first()
    
    if not itinerary:
        return jsonify({"error": "Itinerary item not found"}), 404
    
    return jsonify(itinerary.to_dict()), 200

@app.route('/trips/<int:trip_id>/itinerary/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_itinerary_item(trip_id, item_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    itinerary = Itinerary.query.filter_by(id=item_id, trip_id=trip_id).first()
    
    if not itinerary:
        return jsonify({"error": "Itinerary item not found"}), 404
    
    data = request.get_json()
    
    if 'day' in data:
        itinerary.day = data['day']
    if 'title' in data:
        itinerary.title = data['title']
    if 'description' in data:
        itinerary.description = data['description']
    if 'location' in data:
        itinerary.location = data['location']
    if 'latitude' in data:
        itinerary.latitude = data['latitude']
    if 'longitude' in data:
        itinerary.longitude = data['longitude']
    if 'start_time' in data:
        itinerary.start_time = data['start_time']
    if 'end_time' in data:
        itinerary.end_time = data['end_time']
    
    db.session.commit()
    
    return jsonify({"message": "Itinerary item updated successfully", "itinerary": itinerary.to_dict()}), 200

@app.route('/trips/<int:trip_id>/itinerary/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_itinerary_item(trip_id, item_id):
    user_id = get_jwt_identity()
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    itinerary = Itinerary.query.filter_by(id=item_id, trip_id=trip_id).first()
    
    if not itinerary:
        return jsonify({"error": "Itinerary item not found"}), 404
    
    db.session.delete(itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary item deleted successfully"}), 200

# Routes - User Profile
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user.to_dict()), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Create database and run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database initialized!")
    app.run(debug=True)
