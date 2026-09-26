from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import BusRoute
from datetime import time
import os

class Command(BaseCommand):
    help = 'Seed initial data: admin user + sample routes'

    def handle(self, *args, **kwargs):
        # Create admin — use env vars on Render, fallback for local dev
        admin_pass = os.environ.get('ADMIN_PASSWORD', 'admin123')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@college.edu', admin_pass)
            self.stdout.write(self.style.SUCCESS(f'Admin created: admin / {admin_pass}'))
        else:
            self.stdout.write('Admin already exists — skipping')

        routes = [
            {'route_number': 'R01', 'route_name': 'City Center – College',
             'pickup_points': 'City Bus Stand, Gandhi Nagar, MG Road, Railway Station, College Gate',
             'start_time': time(7, 30), 'end_time': time(8, 30), 'distance_km': 12.5, 'monthly_fee': 650},
            {'route_number': 'R02', 'route_name': 'East Zone – College',
             'pickup_points': 'East Market, Nehru Park, Sector 5, Old Town, College Main Entrance',
             'start_time': time(7, 0), 'end_time': time(8, 15), 'distance_km': 18.0, 'monthly_fee': 850},
            {'route_number': 'R03', 'route_name': 'North Campus Circuit',
             'pickup_points': 'North Bus Depot, Vijay Nagar, Shivaji Park, University Road, College',
             'start_time': time(7, 45), 'end_time': time(8, 45), 'distance_km': 9.0, 'monthly_fee': 500},
            {'route_number': 'R04', 'route_name': 'South Town Express',
             'pickup_points': 'South Gate, Lal Chowk, Bank Colony, ITI Road, College Back Gate',
             'start_time': time(6, 45), 'end_time': time(8, 0), 'distance_km': 22.0, 'monthly_fee': 1000},
        ]

        for r in routes:
            _, created = BusRoute.objects.get_or_create(route_number=r['route_number'], defaults=r)
            self.stdout.write(('Created' if created else 'Exists') + f': Route {r["route_number"]}')

        self.stdout.write(self.style.SUCCESS('Seed complete!'))
