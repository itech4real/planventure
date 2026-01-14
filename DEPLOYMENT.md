# PlanVenture API - Deployment Guide

## Prerequisites
- Python 3.8+
- PostgreSQL 12+ (for production)
- Docker (optional)
- Git

## Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/planventure.git
cd planventure
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
cd planventure-api
pip install -r requirements.txt
```

### 4. Create Environment File
```bash
cp .env.example .env
```

Edit `.env`:
```
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///planventure.db
CORS_ORIGINS=*
LOG_LEVEL=INFO
```

### 5. Initialize Database
```bash
python scripts/create_db.py reset  # Reset database
python scripts/seed_db.py           # Seed test data
```

### 6. Run Development Server
```bash
python app.py
```

Server starts at: `http://localhost:5000`

## Testing

### Run All Tests
```bash
pytest tests/ -v --cov=. --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_endpoints.py -v
```

### Run with Coverage
```bash
pytest --cov=planventure-api --cov-report=term-missing
```

## Production Deployment

### 1. Using Gunicorn

**Install:**
```bash
pip install gunicorn
```

**Create `wsgi.py`:**
```python
from app import app

if __name__ == "__main__":
    app.run()
```

**Run:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### 2. Using Docker

**Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

**Create `.dockerignore`:**
```
.env
__pycache__
*.pyc
.pytest_cache
.venv
.git
```

**Build & Run:**
```bash
docker build -t planventure-api .
docker run -e JWT_SECRET_KEY=your-key -p 5000:5000 planventure-api
```

### 3. Environment Variables (Production)

```bash
# Required
FLASK_ENV=production
JWT_SECRET_KEY=<generate-with: python -c "import secrets; print(secrets.token_hex(32))">
DATABASE_URL=postgresql://user:password@host:5432/planventure

# Optional
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
LOG_LEVEL=WARNING
RATELIMIT_ENABLED=true
RATELIMIT_DEFAULT=50/hour
```

### 4. Database Setup (PostgreSQL)

```sql
-- Create database
CREATE DATABASE planventure;

-- Create user
CREATE USER planventure_user WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE planventure TO planventure_user;
```

Then run:
```bash
DATABASE_URL=postgresql://planventure_user:secure_password@localhost/planventure python scripts/create_db.py
```

### 5. Nginx Configuration

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 6. Systemd Service (Linux)

**Create `/etc/systemd/system/planventure.service`:**

```ini
[Unit]
Description=PlanVenture API
After=network.target

[Service]
Type=notify
User=planventure
WorkingDirectory=/opt/planventure
ExecStart=/opt/planventure/.venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable & Start:**
```bash
sudo systemctl enable planventure
sudo systemctl start planventure
```

## Monitoring

### Check Service Status
```bash
systemctl status planventure
journalctl -u planventure -f
```

### View Logs
```bash
tail -f logs/app.log
```

### Health Check
```bash
curl http://localhost:5000/health
```

## Scaling

### Load Balancing with HAProxy
```
global
    maxconn 4096

frontend api_frontend
    bind *:80
    default_backend api_backend

backend api_backend
    balance roundrobin
    server api1 127.0.0.1:5001
    server api2 127.0.0.1:5002
    server api3 127.0.0.1:5003
```

### Database Backups

```bash
# PostgreSQL
pg_dump -U planventure_user planventure > backup_$(date +%Y%m%d).sql

# Restore
psql -U planventure_user planventure < backup_20240114.sql
```

## CI/CD (GitHub Actions)

**Create `.github/workflows/deploy.yml`:**

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r planventure-api/requirements.txt
      - run: pytest planventure-api/tests/ -v

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Server
        run: |
          # Add your deployment script here
          echo "Deploying..."
```

## Troubleshooting

### Database Connection Error
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"
```

### JWT Token Errors
```bash
# Verify JWT_SECRET_KEY is set
echo $JWT_SECRET_KEY

# Generate new secret
python -c "import secrets; print(secrets.token_hex(32))"
```

### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

## Performance Tuning

### Database Connection Pool
In `config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

### Caching
Add to app.py:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

### Rate Limiting
Configure in config.py:
```python
RATELIMIT_STORAGE_URL = "redis://localhost:6379"
```

## Security Checklist

- [ ] Set strong JWT_SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Set CORS_ORIGINS to specific domains
- [ ] Enable rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable database backups
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated
- [ ] Use strong database password
- [ ] Implement request logging
- [ ] Enable CSRF protection if needed
- [ ] Regular security audits

## Support

For issues or questions, see:
- [README.md](./README.md) - API documentation
- [SUPPORT.md](./SUPPORT.md) - Support guidelines
- Issues: https://github.com/yourusername/planventure/issues
