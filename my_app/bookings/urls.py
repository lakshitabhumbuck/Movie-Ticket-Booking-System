from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView, UserLoginView, MovieListView,
    ShowListView, BookingCreateView, BookingCancelView,
    MyBookingsView, BookingDetailView
)
from .frontend_views import home, my_bookings, api_login, api_signup, api_movies, api_shows, api_book_seat

app_name = 'bookings'

urlpatterns = [
    # Frontend pages
    path('', home, name='home'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    
    # Simple API endpoints for frontend
    path('auth/login/', api_login, name='simple_login'),
    path('auth/signup/', api_signup, name='simple_signup'),
    path('movies/', api_movies, name='simple_movies'),
    path('movies/<int:movie_id>/shows/', api_shows, name='simple_shows'),
    path('shows/<int:show_id>/book/', api_book_seat, name='simple_book'),
    
    # REST API endpoints
    path('signup/', UserRegistrationView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Movie endpoints
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/shows/', ShowListView.as_view(), name='show-list'),
    
    # Booking endpoints
    path('shows/<int:show_id>/book/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:booking_id>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
    path('my-bookings-api/', MyBookingsView.as_view(), name='my-bookings'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
]
