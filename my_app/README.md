# Movie Ticket Booking System

A comprehensive Django REST API for movie ticket booking with JWT authentication, built for a backend developer intern assignment.

## 🚀 Features

- **JWT Authentication**: Secure user registration and login
- **Movie Management**: List all available movies
- **Show Management**: View shows for specific movies
- **Seat Booking**: Book seats with validation and business rules
- **Booking Management**: View and cancel bookings
- **Swagger Documentation**: Complete API documentation
- **Admin Interface**: Django admin for data management
- **Unit Tests**: Comprehensive test coverage

## 🛠 Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: Swagger/OpenAPI (drf-spectacular)
- **Database**: SQLite (default), easily configurable for PostgreSQL/MySQL

## 📋 API Endpoints

### Authentication
- `POST /api/signup/` - Register a new user
- `POST /api/login/` - Login and get JWT tokens
- `POST /api/token/refresh/` - Refresh JWT tokens

### Movies & Shows
- `GET /api/movies/` - List all movies
- `GET /api/movies/<id>/shows/` - List shows for a specific movie

### Bookings
- `POST /api/shows/<id>/book/` - Book a seat for a show
- `POST /api/bookings/<id>/cancel/` - Cancel a booking
- `GET /api/my-bookings/` - List user's bookings
- `GET /api/bookings/<id>/` - Get booking details

### Documentation
- `GET /swagger/` - Swagger UI documentation
- `GET /redoc/` - ReDoc documentation

## 🏗 Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd my_app
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## 🔐 JWT Authentication

### Getting JWT Tokens

1. **Register a new user:**
   ```bash
   curl -X POST http://localhost:8000/api/signup/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpass123",
       "password_confirm": "testpass123",
       "first_name": "Test",
       "last_name": "User"
     }'
   ```

2. **Login to get tokens:**
   ```bash
   curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "testpass123"
     }'
   ```

### Using JWT Tokens

Include the access token in the Authorization header for protected endpoints:
```bash
curl -X GET http://localhost:8000/api/movies/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📖 API Usage Examples

### 1. Register and Login
```bash
# Register
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'

# Login
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### 2. View Movies
```bash
curl -X GET http://localhost:8000/api/movies/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. View Shows for a Movie
```bash
curl -X GET http://localhost:8000/api/movies/1/shows/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Book a Seat
```bash
curl -X POST http://localhost:8000/api/shows/1/book/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "seat_number": 5
  }'
```

### 5. View Your Bookings
```bash
curl -X GET http://localhost:8000/api/my-bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Cancel a Booking
```bash
curl -X POST http://localhost:8000/api/bookings/1/cancel/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📚 Swagger Documentation

Visit `http://localhost:8000/swagger/` for interactive API documentation.

To authenticate in Swagger:
1. Click the "Authorize" button
2. Enter: `Bearer YOUR_ACCESS_TOKEN`
3. Click "Authorize"

## ✅ Business Rules Implemented

- **Double Booking Prevention**: A seat cannot be booked twice for the same show
- **Overbooking Prevention**: Bookings cannot exceed show capacity
- **Seat Validation**: Seat numbers must be within valid range (1 to total_seats)
- **Cancellation**: Cancelling a booking frees up the seat
- **User Authorization**: Users can only cancel their own bookings
- **Show Capacity**: Real-time calculation of available seats

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

The tests cover:
- Model validation and business logic
- API endpoint functionality
- Authentication and authorization
- Booking validation rules
- Error handling

## 🗄 Database Models

### Movie
- `id`: Primary key
- `title`: Movie title (unique)
- `duration_minutes`: Movie duration in minutes
- `created_at`, `updated_at`: Timestamps

### Show
- `id`: Primary key
- `movie`: Foreign key to Movie
- `screen_name`: Name of the screen
- `date_time`: Show date and time
- `total_seats`: Total number of seats
- `created_at`, `updated_at`: Timestamps

### Booking
- `id`: Primary key
- `user`: Foreign key to User
- `show`: Foreign key to Show
- `seat_number`: Seat number
- `status`: 'booked' or 'cancelled'
- `created_at`, `updated_at`: Timestamps

## 🔒 Security Features

- JWT token-based authentication
- User authorization checks
- Input validation and sanitization
- SQL injection prevention (Django ORM)
- CSRF protection
- Secure password handling

## 🚀 Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a production database (PostgreSQL recommended)
3. Set up proper secret key and allowed hosts
4. Configure static files serving
5. Use environment variables for sensitive data
6. Set up SSL/HTTPS
7. Configure proper logging

## 📝 Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to:
- Manage movies and shows
- View and manage bookings
- Monitor system usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is part of a backend developer intern assignment.

---

**API Documentation**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

**ReDoc Documentation**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)