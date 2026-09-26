from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import BusRoute
from datetime import time
import os

class Command(BaseCommand):
    help = 'Seed initial data: admin user + real Bengaluru routes'

    def handle(self, *args, **kwargs):
        # Create admin — use env vars on Render, fallback for local dev
        admin_pass = os.environ.get('ADMIN_PASSWORD', 'admin123')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@college.edu', admin_pass)
            self.stdout.write(self.style.SUCCESS(f'Admin created: admin / {admin_pass}'))
        else:
            self.stdout.write('Admin already exists — skipping')

        routes = [
            {
                'route_number': 'RT-01', 
                'route_name': 'Jayanagar to Campus',
                'pickup_points': 'Jayanagar 4th Block, Banashankari Temple, JP Nagar 3rd Phase, College Gate',
                'start_time': time(7, 30), 
                'end_time': time(8, 45), 
                'distance_km': 18.5, 
                'monthly_fee': 850.00
            },
            {
                'route_number': 'RT-02', 
                'route_name': 'Hebbal to Campus',
                'pickup_points': 'Hebbal Flyover, Hebbal Kempapura, Esteem Mall, College Main Entrance',
                'start_time': time(7, 15), 
                'end_time': time(8, 50), 
                'distance_km': 24.0, 
                'monthly_fee': 1200.00
            },
            {
                'route_number': 'RT-03', 
                'route_name': 'Electronic City to Campus',
                'pickup_points': 'Electronic City Phase 1, Bommasandra, Silk Board, University Road, College',
                'start_time': time(7, 0), 
                'end_time': time(8, 40), 
                'distance_km': 28.5, 
                'monthly_fee': 1500.00
            },
            {
                'route_number': 'RT-04', 
                'route_name': 'Whitefield to Campus',
                'pickup_points': 'Whitefield ITPL, Marathahalli Bridge, KR Puram, College Back Gate',
                'start_time': time(7, 10), 
                'end_time': time(8, 55), 
                'distance_km': 30.0, 
                'monthly_fee': 1400.00
            },
        ]

        for r in routes:
            # update_or_create ensures fees/names update if you change them here
            _, created = BusRoute.objects.update_or_create(
                route_number=r['route_number'], 
                defaults=r
            )
            self.stdout.write(('Created' if created else 'Updated') + f': Route {r["route_number"]} - {r["route_name"]}')

        self.stdout.write(self.style.SUCCESS('Bengaluru route seed complete!'))