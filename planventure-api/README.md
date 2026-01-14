# PlanVenture API

A comprehensive REST API for managing travel plans, trips, and itineraries.

## Features

- **User Management**: Register, login, and manage user profiles
- **Trip Planning**: Create, read, update, and delete trips
- **Itinerary Management**: Add, update, and delete activities for each trip
- **JWT Authentication**: Secure endpoints with JWT tokens
- **Email Validation**: Comprehensive email validation for registration
- **Password Security**: Strong password hashing with salted encryption
- **Rate Limiting**: API rate limiting to prevent abuse
- **CORS Support**: Cross-origin requests allowed
- **Logging**: Comprehensive logging for monitoring and debugging

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/planventure.git
cd planventure/planventure-api
```

### 2. Create and activate virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create .env file
```bash
cp .env.example .env
```

Edit `.env` and set your configuration:
```
FLASK_ENV=development
DATABASE_URL=sqlite:///planventure.db
JWT_SECRET_KEY=your-secret-key-here
```

### 5. Initialize the database
```bash
python create_db.py create
python seed_db.py  # Optional: seed with sample data
```

### 6. Run the server
```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### Health Check
- **GET** `/health` - Check if server is running
  ```bash
  curl http://127.0.0.1:5000/health
  ```

### Authentication

#### Register User
- **POST** `/auth/register`
  ```bash
  curl -X POST http://127.0.0.1:5000/auth/register \
    -H "Content-Type: application/json" \
    -d '{
      "username": "john_doe",
      "email": "john@example.com",
      "password": "StrongPass1!"
    }'
  ```

#### Login
- **POST** `/auth/login`
  ```bash
  curl -X POST http://127.0.0.1:5000/auth/login \
    -H "Content-Type: application/json" \
    -d '{
      "username": "john_doe",
      "password": "StrongPass1!"
    }'
  ```
  Response includes `access_token` and `refresh_token`

#### Get Profile
- **GET** `/profile`
  ```bash
  curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    http://127.0.0.1:5000/profile
  ```

#### Refresh Token
- **POST** `/auth/refresh`
  ```bash
  curl -X POST -H "Authorization: Bearer YOUR_REFRESH_TOKEN" \
    http://127.0.0.1:5000/auth/refresh
  ```

#### Token Info
- **GET** `/auth/token-info`
  ```bash
  curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    http://127.0.0.1:5000/auth/token-info
  ```

### Trips

#### Get All Trips
- **GET** `/trips`
  ```bash
  curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    http://127.0.0.1:5000/trips
  ```

#### Create Trip
- **POST** `/trips`
  ```bash
  curl -X POST http://127.0.0.1:5000/trips \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Summer Vacation",
      "destination": "Paris, France",
      "description": "Amazing trip to Paris",
      "start_date": "2026-06-01T00:00:00",
      "end_date": "2026-06-15T00:00:00"
    }'
  ```

#### Get Trip
- **GET** `/trips/{trip_id}`
  ```bash
  curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    http://127.0.0.1:5000/trips/1
  ```

#### Update Trip
- **PUT** `/trips/{trip_id}`
  ```bash
  curl -X PUT http://127.0.0.1:5000/trips/1 \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Updated Trip Title"
    }'
  ```

#### Delete Trip
- **DELETE** `/trips/{trip_id}`
  ```bash
  curl -X DELETE http://127.0.0.1:5000/trips/1 \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
  ```

### Itinerary

#### Get Itinerary Items
- **GET** `/trips/{trip_id}/itinerary`
  ```bash
  curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    http://127.0.0.1:5000/trips/1/itinerary
  ```

#### Add Itinerary Item
- **POST** `/trips/{trip_id}/itinerary`
  ```bash
  curl -X POST http://127.0.0.1:5000/trips/1/itinerary \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "day": 1,
      "title": "Eiffel Tower Visit",
      "description": "Visit the iconic Eiffel Tower",
      "location": "Eiffel Tower, Paris",
      "latitude": 48.8584,
      "longitude": 2.2945,
      "start_time": "2026-06-01T09:00:00",
      "end_time": "2026-06-01T12:00:00"
    }'
  ```

#### Get Itinerary Item
- **GET** `/trips/{trip_id}/itinerary/{item_id}`
  ```bash
  curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    http://127.0.0.1:5000/trips/1/itinerary/1
  ```

#### Update Itinerary Item
- **PUT** `/trips/{trip_id}/itinerary/{item_id}`
  ```bash
  curl -X PUT http://127.0.0.1:5000/trips/1/itinerary/1 \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "title": "Updated Activity Title"
    }'
  ```

#### Delete Itinerary Item
- **DELETE** `/trips/{trip_id}/itinerary/{item_id}`
  ```bash
  curl -X DELETE http://127.0.0.1:5000/trips/1/itinerary/1 \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
  ```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Tokens are obtained through the `/auth/login` endpoint.

### Token Expiration

- **Access Token**: Valid for 24 hours
- **Refresh Token**: Valid for 30 days

Use the `/auth/refresh` endpoint to get a new access token using your refresh token.

## Password Requirements

Passwords must meet these criteria:
- At least 8 characters long
- Contains uppercase letter (A-Z)
- Contains lowercase letter (a-z)
- Contains digit (0-9)
- Contains special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

Example: `SecurePass123!`

## Email Validation

Emails are validated for:
- Proper RFC format
- Valid domain structure
- Non-disposable email services

## Error Responses

All errors follow a consistent format:

```json
{
  "error": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- **200**: Success
- **201**: Created
- **400**: Bad Request (missing or invalid data)
- **401**: Unauthorized (invalid or missing token)
- **404**: Not Found (resource doesn't exist)
- **409**: Conflict (duplicate username/email)
- **422**: Unprocessable Entity (invalid token claim)
- **500**: Internal Server Error

## Environment Variables

Create a `.env` file in the `planventure-api` directory:

```
# Flask
FLASK_ENV=development  # or production

# Database
DATABASE_URL=sqlite:///planventure.db

# JWT
JWT_SECRET_KEY=your-very-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=24
JWT_REFRESH_TOKEN_EXPIRES=30

# CORS
CORS_ORIGINS=*

# Rate Limiting
RATELIMIT_ENABLED=true
RATELIMIT_DEFAULT=100/hour

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## Testing

### Run Tests
```bash
pytest
```

### Run Tests with Coverage
```bash
pytest --cov=. --cov-report=html
```

### Test with Bruno

1. Open Bruno API client
2. Open the collection: `bruno/PlanVenture API`
3. Select the "Development" environment
4. Run requests in order:
   - Health Check
   - Login
   - Get All Trips
   - Create Trip
   - Add Itinerary Item

## Project Structure

```
planventure-api/
├── app.py              # Main Flask application
├── config.py           # Configuration management
├── logger_config.py    # Logging setup
├── openapi_spec.py     # API documentation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── models/             # Database models
│   ├── __init__.py
│   ├── base.py        # BaseModel with timestamps
│   ├── user.py        # User model
│   └── trip.py        # Trip and Itinerary models
├── utils/             # Utility functions
│   ├── __init__.py
│   ├── password.py    # Password hashing
│   ├── jwt_util.py    # JWT token management
│   └── email_util.py  # Email validation
├── scripts/           # Database management scripts
│   ├── create_db.py
│   ├── db_shell.py
│   └── seed_db.py
└── bruno/            # Bruno collection files
```

## Development

### Code Quality

The project follows PEP 8 style guidelines. Key practices:

- Type hints for function parameters
- Docstrings for classes and functions
- Error handling with try-except blocks
- Input validation before processing
- Logging for debugging and monitoring

### Security

- All passwords are hashed using Werkzeug's pbkdf2:sha256
- JWT tokens have expiration times
- CORS is configured for specified origins
- Email validation prevents disposable addresses
- Rate limiting prevents abuse

## Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Generate a strong `JWT_SECRET_KEY`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Configure proper CORS origins
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Enable rate limiting
- [ ] Configure proper logging
- [ ] Set up monitoring and alerts
- [ ] Implement automated backups

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t planventure-api .
docker run -p 5000:5000 -e FLASK_ENV=production planventure-api
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For support, email support@planventure.com or open an issue on GitHub.

## Roadmap

- [ ] Email verification for new accounts
- [ ] Password reset functionality
- [ ] User profile updates
- [ ] Trip sharing and collaboration
- [ ] Advanced search and filtering
- [ ] Mobile app integration
- [ ] Payment integration for premium features
- [ ] Real-time notifications
