# Movie Ticket Booking System


## 🚀 Features

- **JWT Authentication**: Secure user registration and login
- **Movie Management**: List all available movies
- **Show Management**: View shows for specific movies
- **Seat Booking**: Book seats with validation and business rules
- **Booking Management**: View and cancel bookings
- **Swagger Documentation**: Complete API documentation
- **Admin Interface**: Django admin for data management
-

## 🛠 Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: Swagger/OpenAPI (drf-spectacular)
- **Database**: SQLite 

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

## ✅ Business Rules Implemented

- **Double Booking Prevention**: A seat cannot be booked twice for the same show
- **Overbooking Prevention**: Bookings cannot exceed show capacity
- **Seat Validation**: Seat numbers must be within valid range (1 to total_seats)
- **Cancellation**: Cancelling a booking frees up the seat
- **User Authorization**: Users can only cancel their own bookings
- **Show Capacity**: Real-time calculation of available seats

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


## 📝 Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to:
- Manage movies and shows
- View and manage bookings
- Monitor system usage


---

**API Documentation**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

**ReDoc Documentation**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
