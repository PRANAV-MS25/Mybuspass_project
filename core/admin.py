from django.contrib import admin
from .models import StudentProfile, BusRoute, BusPassApplication

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'roll_number', 'department', 'year', 'phone']
    search_fields = ['user__username', 'roll_number', 'department']

@admin.register(BusRoute)
class BusRouteAdmin(admin.ModelAdmin):
    list_display = ['route_number', 'route_name', 'start_time', 'end_time', 'monthly_fee', 'is_active']
    list_filter = ['is_active']

@admin.register(BusPassApplication)
class BusPassApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'route', 'status', 'total_fee', 'applied_at']
    list_filter = ['status']
    list_editable = ['status']
