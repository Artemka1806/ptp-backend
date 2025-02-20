# Pet The Plant Backend 🌱

A high-performance FastAPI-based backend service for plant monitoring system with real-time metrics tracking and authentication.

## Features
- 🔐 JWT-based authentication
- 📊 Real-time plant metrics via WebSocket
- 🗄️ MongoDB integration with Beanie ODM
- 📱 RESTful API endpoints
- 📄 Swagger/OpenAPI documentation

## Tech Stack
- Python 3.11+
- FastAPI framework
- MongoDB with Beanie ODM
- WebSocket support
- Docker support

## Prerequisites
- Python 3.11+
- MongoDB
- Poetry (recommended) or pip
- Docker (optional)

## Quick Start

### Development
```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start development server
uvicorn app.main:app --reload
```

### Docker
```bash
# Build and run with Docker
docker compose up -d
```

## Environment Configuration
Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=your_password
MONGO_DB_URI=mongodb://root:your_password@mongodb:27017/
MONGO_DB_NAME=db

# JWT Configuration
JWT_SECRET=your_secret_key
JWT_EXPIRATION=120  # Token expiration in minutes

# Optional Development Settings
CORS_ORIGINS=http://localhost:3000
```

> Note: Replace `your_password` and `your_secret_key` with secure values in production.

## API Documentation
After starting the server, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure
```
app/
├── api/         # API endpoints
├── core/        # Core functionality
├── models/      # Database models
├── services/    # Business logic
└── main.py      # Application entry point
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
MIT License - see the [LICENSE](LICENSE) file for details

---
*Part of the Pet The Plant ecosystem - Making plant care smarter* 🪴