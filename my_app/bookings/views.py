from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

from .models import Movie, Show, Booking
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, MovieSerializer,
    ShowSerializer, BookingSerializer, BookingCreateSerializer, UserSerializer
)


class UserRegistrationView(APIView):
    """User registration endpoint"""
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Register a new user",
        description="Create a new user account with username, email, and password",
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(description="User created successfully"),
            400: OpenApiResponse(description="Invalid input data")
        }
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint"""
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Login user",
        description="Authenticate user and return JWT tokens",
        request=UserLoginSerializer,
        responses={
            200: OpenApiResponse(description="Login successful"),
            400: OpenApiResponse(description="Invalid credentials")
        }
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieListView(generics.ListAPIView):
    """List all movies"""
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get all movies",
        description="Retrieve a list of all available movies",
        responses={200: MovieSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ShowListView(generics.ListAPIView):
    """List shows for a specific movie"""
    serializer_class = ShowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        return Show.objects.filter(movie_id=movie_id)

    @extend_schema(
        summary="Get shows for a movie",
        description="Retrieve all shows for a specific movie",
        parameters=[
            OpenApiParameter(
                name='movie_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Movie ID'
            )
        ],
        responses={200: ShowSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookingCreateView(APIView):
    """Create a new booking"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Book a seat",
        description="Book a seat for a specific show",
        parameters=[
            OpenApiParameter(
                name='show_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Show ID'
            )
        ],
        request=BookingCreateSerializer,
        responses={
            201: OpenApiResponse(description="Booking created successfully"),
            400: OpenApiResponse(description="Invalid input or seat already booked"),
            404: OpenApiResponse(description="Show not found")
        }
    )
    def post(self, request, show_id):
        show = get_object_or_404(Show, id=show_id)
        serializer = BookingCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            seat_number = serializer.validated_data['seat_number']
            
            # Check if seat number is valid for this show
            if seat_number > show.total_seats:
                return Response({
                    'error': f'Seat number {seat_number} exceeds total seats {show.total_seats}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if seat is already booked
            if Booking.objects.filter(show=show, seat_number=seat_number, status='booked').exists():
                return Response({
                    'error': f'Seat {seat_number} is already booked for this show'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create booking with atomic transaction
            try:
                with transaction.atomic():
                    booking = Booking.objects.create(
                        user=request.user,
                        show=show,
                        seat_number=seat_number,
                        status='booked'
                    )
                    booking_serializer = BookingSerializer(booking)
                    return Response(booking_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    'error': 'Failed to create booking. Please try again.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookingCancelView(APIView):
    """Cancel a booking"""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Cancel a booking",
        description="Cancel an existing booking",
        parameters=[
            OpenApiParameter(
                name='booking_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Booking ID'
            )
        ],
        responses={
            200: OpenApiResponse(description="Booking cancelled successfully"),
            400: OpenApiResponse(description="Cannot cancel this booking"),
            404: OpenApiResponse(description="Booking not found")
        }
    )
    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        
        # Security check: Only the booking owner can cancel
        if booking.user != request.user:
            return Response({
                'error': 'You can only cancel your own bookings'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Check if booking can be cancelled
        if booking.status == 'cancelled':
            return Response({
                'error': 'Booking is already cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Cancel the booking
        booking.status = 'cancelled'
        booking.save()
        
        serializer = BookingSerializer(booking)
        return Response({
            'message': 'Booking cancelled successfully',
            'booking': serializer.data
        }, status=status.HTTP_200_OK)


class MyBookingsView(generics.ListAPIView):
    """List all bookings for the logged-in user"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

    @extend_schema(
        summary="Get user bookings",
        description="Retrieve all bookings for the authenticated user",
        responses={200: BookingSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookingDetailView(generics.RetrieveAPIView):
    """Get details of a specific booking"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    @extend_schema(
        summary="Get booking details",
        description="Retrieve details of a specific booking",
        responses={200: BookingSerializer, 404: OpenApiResponse(description="Booking not found")}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)