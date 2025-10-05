from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Movie, Show, Booking


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model"""
    class Meta:
        model = Movie
        fields = ['id', 'title', 'duration_minutes', 'created_at', 'updated_at']


class ShowSerializer(serializers.ModelSerializer):
    """Serializer for Show model"""
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)
    available_seats = serializers.ReadOnlyField()
    is_fully_booked = serializers.ReadOnlyField()

    class Meta:
        model = Show
        fields = ['id', 'movie', 'movie_id', 'screen_name', 'date_time', 'total_seats', 
                 'available_seats', 'is_fully_booked', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    user = serializers.StringRelatedField(read_only=True)
    show = ShowSerializer(read_only=True)
    show_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'show', 'show_id', 'seat_number', 'status', 
                 'created_at', 'updated_at']

    def validate_seat_number(self, value):
        """Validate seat number"""
        show_id = self.initial_data.get('show_id')
        if show_id:
            try:
                show = Show.objects.get(id=show_id)
                if value > show.total_seats:
                    raise serializers.ValidationError(
                        f'Seat number {value} exceeds total seats {show.total_seats}'
                    )
                if value < 1:
                    raise serializers.ValidationError('Seat number must be at least 1')
            except Show.DoesNotExist:
                raise serializers.ValidationError('Invalid show ID')
        return value

    def validate(self, attrs):
        """Custom validation for booking"""
        show_id = attrs.get('show_id')
        seat_number = attrs.get('seat_number')

        if show_id and seat_number:
            # Check if seat is already booked
            existing_booking = Booking.objects.filter(
                show_id=show_id,
                seat_number=seat_number,
                status='booked'
            )
            
            if self.instance:  # Updating existing booking
                existing_booking = existing_booking.exclude(pk=self.instance.pk)
            
            if existing_booking.exists():
                raise serializers.ValidationError(
                    f'Seat {seat_number} is already booked for this show'
                )

        return attrs


class BookingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating bookings"""
    class Meta:
        model = Booking
        fields = ['seat_number']

    def validate_seat_number(self, value):
        """Validate seat number"""
        if value < 1:
            raise serializers.ValidationError('Seat number must be at least 1')
        return value


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
