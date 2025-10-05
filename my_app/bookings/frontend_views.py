from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json

from rest_framework_simplejwt.tokens import RefreshToken
from .models import Movie, Show, Booking


def home(request):
    """Simple home page with movie listings"""
    return render(request, 'bookings/home.html')


def my_bookings(request):
    """Simple my bookings page"""
    return render(request, 'bookings/my_bookings.html')


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """Simple login API"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                },
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_signup(request):
    """Simple signup API"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def api_movies(request):
    """Simple movies API"""
    try:
        movies = Movie.objects.all()
        movies_data = []
        for movie in movies:
            movies_data.append({
                'id': movie.id,
                'title': movie.title,
                'duration_minutes': movie.duration_minutes,
                'created_at': movie.created_at.isoformat(),
                'updated_at': movie.updated_at.isoformat(),
            })
        return JsonResponse(movies_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def api_shows(request, movie_id):
    """Simple shows API"""
    try:
        shows = Show.objects.filter(movie_id=movie_id)
        shows_data = []
        for show in shows:
            shows_data.append({
                'id': show.id,
                'movie': {
                    'id': show.movie.id,
                    'title': show.movie.title,
                    'duration_minutes': show.movie.duration_minutes,
                },
                'screen_name': show.screen_name,
                'date_time': show.date_time.isoformat(),
                'total_seats': show.total_seats,
                'available_seats': show.available_seats,
                'is_fully_booked': show.is_fully_booked,
                'created_at': show.created_at.isoformat(),
                'updated_at': show.updated_at.isoformat(),
            })
        return JsonResponse(shows_data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_book_seat(request, show_id):
    """Simple book seat API"""
    try:
        data = json.loads(request.body)
        seat_number = data.get('seat_number')
        
        if not seat_number:
            return JsonResponse({'error': 'Seat number is required'}, status=400)
        
        # Get user from token (simplified)
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # For simplicity, we'll use a mock user or get from token
        # In a real app, you'd decode the JWT token
        try:
            from rest_framework_simplejwt.authentication import JWTAuthentication
            jwt_auth = JWTAuthentication()
            user, _ = jwt_auth.authenticate(request)
        except:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        
        show = Show.objects.get(id=show_id)
        
        # Check if seat is valid
        if seat_number > show.total_seats or seat_number < 1:
            return JsonResponse({'error': f'Seat number {seat_number} is not valid'}, status=400)
        
        # Check if seat is already booked
        existing_booking = Booking.objects.filter(
            show=show,
            seat_number=seat_number,
            status='booked'
        ).exists()
        
        if existing_booking:
            return JsonResponse({'error': f'Seat {seat_number} is already booked'}, status=400)
        
        # Create booking
        booking = Booking.objects.create(
            user=user,
            show=show,
            seat_number=seat_number,
            status='booked'
        )
        
        return JsonResponse({
            'id': booking.id,
            'user': booking.user.username,
            'show': {
                'id': booking.show.id,
                'movie': {
                    'id': booking.show.movie.id,
                    'title': booking.show.movie.title,
                },
                'screen_name': booking.show.screen_name,
                'date_time': booking.show.date_time.isoformat(),
            },
            'seat_number': booking.seat_number,
            'status': booking.status,
            'created_at': booking.created_at.isoformat(),
        })
    except Show.DoesNotExist:
        return JsonResponse({'error': 'Show not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
