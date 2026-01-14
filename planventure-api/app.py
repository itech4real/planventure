from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import configuration and logging
from config import config
from logger_config import logger

# Import models and utilities
from models import db, User, Trip, Itinerary
from utils import JWTUtility
from utils.email_verification import EmailVerificationUtility

app = Flask(__name__)

# Load configuration
app.config.from_object(config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)
CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[app.config.get('RATELIMIT_DEFAULT', '100/hour')]
)

logger.info(f"Flask app initialized in {app.config.get('ENV', 'development')} mode")

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
    
    # Generate verification token and send email
    verification_token = EmailVerificationUtility.create_verification_token(user.email)
    EmailVerificationUtility.send_verification_email(user.email, verification_token)
    
    tokens = JWTUtility.create_tokens(user.id)
    
    return jsonify({
        "message": "User created successfully. Please verify your email.",
        "user": user.to_dict(),
        **tokens
    }), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    try:
        tokens = JWTUtility.create_tokens(user.id)
        return jsonify({
            "message": "Login successful",
            "user": user.to_dict(),
            **tokens
        }), 200
    except Exception as e:
        return jsonify({"error": f"Token generation failed: {str(e)}"}), 500

@app.route('/auth/verify-email', methods=['POST'])
def verify_email():
    """Verify user's email using verification token."""
    data = request.get_json()
    token = data.get('token') if data else None
    
    if not token:
        return jsonify({"error": "Verification token is required"}), 400
    
    decoded = EmailVerificationUtility.verify_email_token(token)
    
    if not decoded:
        return jsonify({"error": "Invalid or expired verification token"}), 400
    
    user = User.query.filter_by(email=decoded.get('email')).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user.email_verified = True
    db.session.commit()
    
    return jsonify({"message": "Email verified successfully"}), 200

@app.route('/auth/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email to user."""
    data = request.get_json()
    email = data.get('email') if data else None
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user.email_verified:
        return jsonify({"message": "Email already verified"}), 200
    
    verification_token = EmailVerificationUtility.create_verification_token(user.email)
    EmailVerificationUtility.send_verification_email(user.email, verification_token)
    
    return jsonify({"message": "Verification email sent"}), 200

@app.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset via email."""
    data = request.get_json()
    email = data.get('email') if data else None
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    # Don't reveal if email exists or not for security
    if user:
        reset_token = EmailVerificationUtility.create_verification_token(user.email)
        EmailVerificationUtility.send_password_reset_email(user.email, reset_token)
    
    return jsonify({"message": "If email exists, password reset link has been sent"}), 200

@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """Reset password using token."""
    data = request.get_json()
    token = data.get('token') if data else None
    new_password = data.get('new_password') if data else None
    
    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400
    
    decoded = EmailVerificationUtility.verify_email_token(token)
    
    if not decoded:
        return jsonify({"error": "Invalid or expired reset token"}), 400
    
    user = User.query.filter_by(email=decoded.get('email')).first()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({"message": "Password reset successfully"}), 200

# Routes - Trips
@app.route('/trips', methods=['GET'])
@jwt_required()
def get_trips():
    user_id = int(get_jwt_identity())
    trips = Trip.query.filter_by(user_id=user_id).all()
    return jsonify([trip.to_dict() for trip in trips]), 200

@app.route('/trips', methods=['POST'])
@jwt_required()
def create_trip():
    user_id = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    return jsonify(trip.to_dict()), 200

@app.route('/trips/<int:trip_id>', methods=['PUT'])
@jwt_required()
def update_trip(trip_id):
    user_id = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    itineraries = Itinerary.query.filter_by(trip_id=trip_id).order_by(Itinerary.day).all()
    return jsonify([item.to_dict() for item in itineraries]), 200

@app.route('/trips/<int:trip_id>/itinerary', methods=['POST'])
@jwt_required()
def create_itinerary_item(trip_id):
    user_id = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
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
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    itinerary = Itinerary.query.filter_by(id=item_id, trip_id=trip_id).first()
    
    if not itinerary:
        return jsonify({"error": "Itinerary item not found"}), 404
    
    db.session.delete(itinerary)
    db.session.commit()
    
    return jsonify({"message": "Itinerary item deleted successfully"}), 200

# Routes - Trip Sharing & Collaboration
@app.route('/trips/<int:trip_id>/share', methods=['POST'])
@jwt_required()
def share_trip(trip_id):
    """Share a trip with another user."""
    from models import TripShare
    
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    data = request.get_json()
    share_with_email = data.get('email') if data else None
    permission = data.get('permission', 'view') if data else 'view'
    
    if not share_with_email:
        return jsonify({"error": "Email is required"}), 400
    
    shared_user = User.query.filter_by(email=share_with_email).first()
    if not shared_user:
        return jsonify({"error": "User not found"}), 404
    
    existing = TripShare.query.filter_by(trip_id=trip_id, shared_with_user_id=shared_user.id).first()
    if existing:
        return jsonify({"error": "Trip already shared with this user"}), 409
    
    share = TripShare(trip_id=trip_id, shared_with_user_id=shared_user.id, permission=permission)
    db.session.add(share)
    db.session.commit()
    
    return jsonify({"message": "Trip shared successfully", "share": share.to_dict()}), 201

@app.route('/trips/shared', methods=['GET'])
@jwt_required()
def get_shared_trips():
    """Get trips shared with the current user."""
    from models import TripShare
    
    user_id = int(get_jwt_identity())
    shares = TripShare.query.filter_by(shared_with_user_id=user_id).all()
    
    return jsonify([share.to_dict() for share in shares]), 200

@app.route('/trips/<int:trip_id>/share/<int:shared_user_id>', methods=['DELETE'])
@jwt_required()
def unshare_trip(trip_id, shared_user_id):
    """Remove sharing for a trip."""
    from models import TripShare
    
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    share = TripShare.query.filter_by(trip_id=trip_id, shared_with_user_id=shared_user_id).first()
    if not share:
        return jsonify({"error": "Share not found"}), 404
    
    db.session.delete(share)
    db.session.commit()
    
    return jsonify({"message": "Trip sharing removed"}), 200

# Routes - Expense Tracking
@app.route('/trips/<int:trip_id>/expenses', methods=['GET'])
@jwt_required()
def get_expenses(trip_id):
    """Get all expenses for a trip."""
    from models import Expense
    
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    expenses = Expense.query.filter_by(trip_id=trip_id).all()
    return jsonify([expense.to_dict() for expense in expenses]), 200

@app.route('/trips/<int:trip_id>/expenses', methods=['POST'])
@jwt_required()
def create_expense(trip_id):
    """Add an expense to a trip."""
    from models import Expense
    
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    data = request.get_json()
    
    if not data or not data.get('category') or not data.get('amount'):
        return jsonify({"error": "Missing required fields"}), 400
    
    expense = Expense(
        trip_id=trip_id,
        paid_by_user_id=user_id,
        category=data['category'],
        description=data.get('description'),
        amount=data['amount'],
        currency=data.get('currency', 'USD'),
        date=data.get('date')
    )
    
    db.session.add(expense)
    db.session.commit()
    
    return jsonify({"message": "Expense created", "expense": expense.to_dict()}), 201

@app.route('/trips/<int:trip_id>/expenses/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(trip_id, expense_id):
    """Update an expense."""
    from models import Expense
    
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    expense = Expense.query.filter_by(id=expense_id, trip_id=trip_id).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    
    data = request.get_json()
    
    if 'category' in data:
        expense.category = data['category']
    if 'amount' in data:
        expense.amount = data['amount']
    if 'description' in data:
        expense.description = data['description']
    if 'currency' in data:
        expense.currency = data['currency']
    if 'date' in data:
        expense.date = data['date']
    
    db.session.commit()
    
    return jsonify({"message": "Expense updated", "expense": expense.to_dict()}), 200

@app.route('/trips/<int:trip_id>/expenses/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(trip_id, expense_id):
    """Delete an expense."""
    from models import Expense
    
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    expense = Expense.query.filter_by(id=expense_id, trip_id=trip_id).first()
    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify({"message": "Expense deleted"}), 200

# Routes - Trip Search & Filtering
@app.route('/trips/search', methods=['GET'])
@jwt_required()
def search_trips():
    """Search and filter user's trips."""
    user_id = int(get_jwt_identity())
    
    # Get query parameters
    search = request.args.get('q', '')
    destination = request.args.get('destination', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    
    query = Trip.query.filter_by(user_id=user_id)
    
    if search:
        query = query.filter(Trip.title.ilike(f'%{search}%') | Trip.description.ilike(f'%{search}%'))
    
    if destination:
        query = query.filter(Trip.destination.ilike(f'%{destination}%'))
    
    if start_date:
        query = query.filter(Trip.start_date >= start_date)
    
    if end_date:
        query = query.filter(Trip.end_date <= end_date)
    
    trips = query.all()
    
    return jsonify([trip.to_dict() for trip in trips]), 200

# Routes - Trip Templates
@app.route('/templates', methods=['GET'])
def get_templates():
    """Get all public trip templates."""
    from models import TripTemplate
    
    templates = TripTemplate.query.filter_by(is_public=True).all()
    return jsonify([template.to_dict() for template in templates]), 200

@app.route('/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    """Get a specific trip template."""
    from models import TripTemplate
    
    template = TripTemplate.query.get(template_id)
    if not template or (not template.is_public and (not template.created_by_user_id)):
        return jsonify({"error": "Template not found"}), 404
    
    return jsonify(template.to_dict()), 200

@app.route('/trips/<int:trip_id>/from-template/<int:template_id>', methods=['POST'])
@jwt_required()
def create_trip_from_template(trip_id, template_id):
    """Create itinerary items from a template."""
    from models import TripTemplate, TemplateItinerary
    
    user_id = int(get_jwt_identity())
    trip = Trip.query.filter_by(id=trip_id, user_id=user_id).first()
    
    if not trip:
        return jsonify({"error": "Trip not found"}), 404
    
    template = TripTemplate.query.get(template_id)
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    # Create itinerary items from template
    for template_item in template.template_items:
        itinerary = Itinerary(
            trip_id=trip_id,
            day=template_item.day,
            title=template_item.title,
            description=template_item.description,
            location=template_item.location
        )
        db.session.add(itinerary)
    
    db.session.commit()
    
    return jsonify({"message": "Trip created from template"}), 201

# Routes - User Profile
@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Return the current authenticated user's profile."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200

@app.route('/profile', methods=['PATCH', 'PUT'])
@jwt_required()
def update_profile():
    """Update the current user's profile."""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if 'username' in data:
        # Check if new username is already taken
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "Username already taken"}), 409
        user.username = data['username']

    db.session.commit()

    return jsonify({"message": "Profile updated successfully", "user": user.to_dict()}), 200

# Routes - Token Management
@app.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """Refresh access token using refresh token."""
    user_id = int(get_jwt_identity())

    try:
        access_token = JWTUtility.create_access_token(user_id)
        return jsonify({
            "message": "Token refreshed successfully",
            "access_token": access_token,
            "token_type": "Bearer"
        }), 200
    except Exception as e:
        return jsonify({"error": f"Token refresh failed: {str(e)}"}), 500


@app.route('/auth/token-info', methods=['GET'])
@jwt_required()
def token_info():
    """Get information about the current token."""
    user_id = int(get_jwt_identity())

    # Get token from request header
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace('Bearer ', '')

    try:
        expiry_time = JWTUtility.get_token_expiry_time(token)
        time_remaining = JWTUtility.get_time_until_expiry(token)

        return jsonify({
            "user_id": user_id,
            "expires_at": expiry_time.isoformat() if expiry_time else None,
            "expires_in_seconds": time_remaining.total_seconds() if time_remaining else None,
            "is_expired": JWTUtility.is_token_expired(token)
        }), 200
    except Exception as e:
        return jsonify({"error": f"Cannot retrieve token info: {str(e)}"}), 400

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
    app.run(debug=False, use_reloader=False)
