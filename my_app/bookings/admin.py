from django.contrib import admin
from .models import Movie, Show, Booking


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration_minutes', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['movie', 'screen_name', 'date_time', 'total_seats', 'available_seats', 'is_fully_booked']
    list_filter = ['movie', 'screen_name', 'date_time']
    search_fields = ['movie__title', 'screen_name']
    readonly_fields = ['available_seats', 'is_fully_booked', 'created_at', 'updated_at']
    
    def available_seats(self, obj):
        return obj.available_seats
    available_seats.short_description = 'Available Seats'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'show', 'seat_number', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'show__movie']
    search_fields = ['user__username', 'show__movie__title', 'seat_number']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'show', 'show__movie')