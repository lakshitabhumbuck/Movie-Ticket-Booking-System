from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from bookings.models import Movie, Show


class Command(BaseCommand):
    help = 'Populate database with sample movies and shows'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample movies
        movies_data = [
            {'title': 'The Dark Knight', 'duration_minutes': 152},
            {'title': 'Inception', 'duration_minutes': 148},
            {'title': 'Interstellar', 'duration_minutes': 169},
            {'title': 'The Matrix', 'duration_minutes': 136},
            {'title': 'Avatar', 'duration_minutes': 162},
        ]
        
        movies = []
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={'duration_minutes': movie_data['duration_minutes']}
            )
            movies.append(movie)
            if created:
                self.stdout.write(f'Created movie: {movie.title}')
        
        # Create sample shows - fewer shows for simplicity
        screens = ['Screen 1', 'Screen 2']
        base_time = timezone.now() + timedelta(hours=2)
        
        show_count = 0
        for movie in movies:
            for screen in screens:
                for day_offset in range(3):  # 3 days of shows
                    for time_offset in range(2):  # 2 shows per day
                        show_time = base_time + timedelta(
                            days=day_offset,
                            hours=time_offset * 6 + 12  # 12 PM, 6 PM
                        )
                        
                        show, created = Show.objects.get_or_create(
                            movie=movie,
                            screen_name=screen,
                            date_time=show_time,
                            defaults={'total_seats': 50}  # Smaller venue for testing
                        )
                        
                        if created:
                            show_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(movies)} movies and {show_count} shows'
            )
        )
