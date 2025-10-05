from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Movie, Show, Booking


class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            duration_minutes=120
        )

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, "Test Movie")
        self.assertEqual(self.movie.duration_minutes, 120)
        self.assertTrue(self.movie.created_at)

    def test_movie_str_representation(self):
        expected = "Test Movie (120 min)"
        self.assertEqual(str(self.movie), expected)


class ShowModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            duration_minutes=120
        )
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name="Screen 1",
            date_time=timezone.now() + timedelta(days=1),
            total_seats=100
        )

    def test_show_creation(self):
        self.assertEqual(self.show.movie, self.movie)
        self.assertEqual(self.show.screen_name, "Screen 1")
        self.assertEqual(self.show.total_seats, 100)

    def test_available_seats_calculation(self):
        # Initially all seats should be available
        self.assertEqual(self.show.available_seats, 100)

    def test_is_fully_booked(self):
        # Initially should not be fully booked
        self.assertFalse(self.show.is_fully_booked)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            duration_minutes=120
        )
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name="Screen 1",
            date_time=timezone.now() + timedelta(days=1),
            total_seats=100
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            show=self.show,
            seat_number=1,
            status='booked'
        )
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.show, self.show)
        self.assertEqual(booking.seat_number, 1)
        self.assertEqual(booking.status, 'booked')

    def test_booking_str_representation(self):
        booking = Booking.objects.create(
            user=self.user,
            show=self.show,
            seat_number=1,
            status='booked'
        )
        expected = f"{self.user.username} - Seat 1 for {self.show}"
        self.assertEqual(str(booking), expected)

    def test_double_booking_prevention(self):
        # Create first booking
        Booking.objects.create(
            user=self.user,
            show=self.show,
            seat_number=1,
            status='booked'
        )
        
        # Try to create second booking for same seat
        with self.assertRaises(Exception):
            Booking.objects.create(
                user=self.user,
                show=self.show,
                seat_number=1,
                status='booked'
            )


class AuthenticationAPITest(APITestCase):
    def setUp(self):
        self.signup_url = reverse('bookings:signup')
        self.login_url = reverse('bookings:login')

    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        # Create user first
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_invalid_login(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MovieAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            duration_minutes=120
        )
        self.movies_url = reverse('bookings:movie-list')
        
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_movies_list(self):
        response = self.client.get(self.movies_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Movie')


class ShowAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            duration_minutes=120
        )
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name="Screen 1",
            date_time=timezone.now() + timedelta(days=1),
            total_seats=100
        )
        
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_get_shows_for_movie(self):
        url = reverse('bookings:show-list', kwargs={'movie_id': self.movie.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['screen_name'], 'Screen 1')


class BookingAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            duration_minutes=120
        )
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name="Screen 1",
            date_time=timezone.now() + timedelta(days=1),
            total_seats=100
        )
        
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_booking(self):
        url = reverse('bookings:booking-create', kwargs={'show_id': self.show.id})
        data = {'seat_number': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Booking.objects.filter(show=self.show, seat_number=1).exists())

    def test_double_booking_prevention(self):
        # Create first booking
        Booking.objects.create(
            user=self.user,
            show=self.show,
            seat_number=1,
            status='booked'
        )
        
        # Try to create second booking for same seat
        url = reverse('bookings:booking-create', kwargs={'show_id': self.show.id})
        data = {'seat_number': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already booked', response.data['error'])

    def test_invalid_seat_number(self):
        url = reverse('bookings:booking-create', kwargs={'show_id': self.show.id})
        data = {'seat_number': 101}  # Exceeds total seats
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_booking(self):
        # Create a booking first
        booking = Booking.objects.create(
            user=self.user,
            show=self.show,
            seat_number=1,
            status='booked'
        )
        
        url = reverse('bookings:booking-cancel', kwargs={'booking_id': booking.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if booking is cancelled
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'cancelled')

    def test_get_my_bookings(self):
        # Create a booking
        Booking.objects.create(
            user=self.user,
            show=self.show,
            seat_number=1,
            status='booked'
        )
        
        url = reverse('bookings:my-bookings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_cannot_cancel_others_booking(self):
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        # Create booking for other user
        booking = Booking.objects.create(
            user=other_user,
            show=self.show,
            seat_number=1,
            status='booked'
        )
        
        url = reverse('bookings:booking-cancel', kwargs={'booking_id': booking.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_access(self):
        # Remove authentication
        self.client.credentials()
        
        url = reverse('bookings:booking-create', kwargs={'show_id': self.show.id})
        data = {'seat_number': 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)