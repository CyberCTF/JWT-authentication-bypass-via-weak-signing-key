# InventoryPro Technical Documentation

## Architecture

InventoryPro is built using a modern web architecture with the following components:

### Backend Stack
- **Framework**: Flask 2.3.3
- **Authentication**: PyJWT 2.8.0
- **Server**: Gunicorn 21.2.0
- **Language**: Python 3.11

### Frontend Stack
- **CSS Framework**: TailwindCSS
- **Template Engine**: Jinja2
- **Design System**: Dark theme with glassmorphism
- **Responsive**: Mobile-first approach

### Deployment
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Port**: 3206 (external) → 5000 (internal)
- **Environment**: Production-ready

## Authentication System

### JWT Implementation
The application uses JSON Web Tokens (JWT) for session management:

```python
JWT_SECRET = "admin123"  # Configuration
JWT_ALGORITHM = "HS256"  # HMAC SHA-256
```

### Token Structure
```json
{
  "iss": "inventorymanager",
  "exp": 1756992207,
  "sub": "username",
  "role": "user_role",
  "kid": "unique_key_id"
}
```

### Security Configuration
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 24 hours
- **Storage**: HTTPOnly cookies
- **Validation**: Server-side verification

## API Endpoints

### Public Routes
- `GET /` - Login page
- `POST /login` - Authentication endpoint

### Protected Routes
- `GET /dashboard` - Main inventory dashboard
- `GET /my-account` - User profile page
- `GET /logout` - Session termination

### Admin Routes
- `GET /admin` - Admin panel (restricted)
- `GET /admin/delete` - User management (admin only)

## Database Schema

### Users Collection
```python
users = {
    "username": {
        "password": "hashed_password",
        "role": "user_role"
    }
}
```

### Inventory Items
```python
inventory_items = [
    {
        "id": int,
        "name": str,
        "category": str,
        "quantity": int,
        "location": str,
        "status": str
    }
]
```

### Critical Assets (Admin Only)
```python
critical_assets = [
    {
        "id": int,
        "name": str,
        "value": str,
        "location": str,
        "flag": str  # Security tokens
    }
]
```

## Security Features

### Role-Based Access Control
- **Manager**: Standard inventory access
- **Supervisor**: Enhanced reporting
- **Admin**: Full system control

### Session Management
- JWT token validation on each request
- Automatic session expiration
- Secure cookie configuration

### Input Validation
- Form data sanitization
- SQL injection prevention
- XSS protection

## Deployment Configuration

### Docker Configuration
```dockerfile
FROM python:3.11-slim
WORKDIR /app
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Environment Variables
- `FLASK_ENV=production`
- `JWT_SECRET=admin123`

### Health Monitoring
- Container health checks enabled
- Automatic restart on failure
- Performance monitoring

## Development

### Local Setup
```bash
cd build
pip install -r requirements.txt
python app.py
```

### Testing
```bash
cd test
python -m pytest test_app.py -v
```

### Building
```bash
cd deploy
docker-compose build
docker-compose up -d
```

## Performance Optimization

- **Gunicorn**: Multi-worker deployment
- **Static Assets**: Optimized delivery
- **Response Caching**: Browser caching headers
- **Compression**: Gzip compression enabled

## Monitoring and Logging

- Application logs to stdout
- Container health status
- Performance metrics
- Error tracking

## Security Considerations

- Regular dependency updates
- Security scanning
- Access log monitoring
- Incident response procedures
