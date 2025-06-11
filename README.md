# AuthFast

A modern, fast, and secure authentication API built with FastAPI. AuthFast provides a complete user authentication system with email verification, JWT tokens, and a robust REST API.

## 🚀 Features

- **User Registration & Authentication**: Secure user registration with email verification
- **JWT Token-based Authentication**: Stateless authentication using JSON Web Tokens
- **Email Verification**: Automated email verification system using SendGrid
- **Password Security**: Bcrypt password hashing for secure credential storage
- **Database Integration**: PostgreSQL with SQLAlchemy and Alembic migrations
- **Docker Support**: Containerized application with Docker Compose
- **Health Checks**: Built-in health monitoring endpoints
- **Admin User Management**: Automatic admin user creation via bootstrap

## 🛠️ Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python web framework
- **Database**: [PostgreSQL](https://www.postgresql.org/) - Robust relational database
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) + [SQLModel](https://sqlmodel.tiangolo.com/) - Type-safe database interactions
- **Authentication**: [JWT](https://jwt.io/) tokens with [PyJWT](https://pyjwt.readthedocs.io/)
- **Password Hashing**: [Passlib](https://passlib.readthedocs.io/) with bcrypt
- **Email Service**: [SendGrid](https://sendgrid.com/) API integration
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/) database migrations
- **Containerization**: [Docker](https://www.docker.com/) & Docker Compose
- **Dependency Management**: [Poetry](https://python-poetry.org/)
- **Code Quality**: [Ruff](https://beta.ruff.rs/) for linting and formatting

## 📋 API Endpoints

### Authentication (`/api/auth`)
- `POST /api/auth/login` - User login with username/password
- `POST /api/auth/register` - User registration
- `POST /api/auth/resend_email_verification` - Resend email verification
- `GET /api/auth/verify_email` - Verify email with token

### Users (`/api/users`)
- `GET /api/users/me` - Get current user profile (requires authentication)

### Health
- `GET /health` - Health check endpoint

## 🚀 Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation) (for local development)
- Python 3.11+

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd authfast
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   
   Update the `.env` file with your configuration:
   ```env
   # Database
   POSTGRES_USER=matt
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=app

   # Admin User
   ADMIN_EMAIL=admin@example.com
   ADMIN_USERNAME=admin
   ADMIN_FULL_NAME=Administrator
   ADMIN_PASSWORD=admin_password
   ADMIN_HASHED_PASSWORD=<bcrypt_hash_of_admin_password>

   # SendGrid
   SENDGRID_API_KEY=your_sendgrid_api_key

   # Application
   APPLICATION_HOSTNAME=http://localhost:5001
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

### Running with Docker (Recommended)

1. **Start the application**
   ```bash
   docker-compose up -d
   ```

2. **Check the application is running**
   ```bash
   curl http://localhost:5001/health
   ```

3. **Access the API documentation**
   - Interactive API docs: http://localhost:5001/docs
   - Alternative docs: http://localhost:5001/redoc

### Local Development Setup

1. **Install dependencies**
   ```bash
   poetry install
   ```

2. **Start PostgreSQL database**
   ```bash
   docker-compose up -d db
   ```

3. **Run database migrations**
   ```bash
   poetry run alembic upgrade head
   ```

4. **Start the development server**
   ```bash
   poetry run fastapi dev app/main.py --host 0.0.0.0 --port 5001
   ```

## 🧪 Testing

Run the test suite:
```bash
poetry run pytest
```

Run tests with coverage:
```bash
poetry run pytest --cov=app
```

## 📁 Project Structure

```
authfast/
├── app/
│   ├── controllers/         # Business logic controllers
│   ├── dependencies/        # FastAPI dependencies
│   ├── models/             # SQLModel data models
│   ├── routers/            # API route handlers
│   ├── scripts/            # Utility scripts (bootstrap, etc.)
│   ├── templates/          # Email templates
│   ├── config.py           # Application configuration
│   ├── logger.py           # Logging configuration
│   └── main.py            # FastAPI application entry point
├── alembic/               # Database migration files
├── tests/                 # Test suite
├── docker-compose.yaml    # Docker services configuration
├── Dockerfile            # Application container image
├── pyproject.toml        # Python project configuration
└── README.md            # This file
```

## 🔧 Configuration

The application uses environment variables for configuration. Key settings include:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT token signing
- `SENDGRID_API_KEY`: SendGrid API key for email services
- `APPLICATION_HOSTNAME`: Base URL for email links
- Admin user settings for initial user creation

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
2. **Build and run with docker-compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Database Migrations

Run migrations in production:
```bash
docker-compose exec web poetry run alembic upgrade head
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the API documentation at `/docs` endpoint
- Review the health check endpoint at `/health`
