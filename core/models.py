from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year = models.IntegerField(choices=[(1,'1st Year'),(2,'2nd Year'),(3,'3rd Year'),(4,'4th Year')])
    phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_number})"


class BusRoute(models.Model):
    route_number = models.CharField(max_length=20, unique=True)
    route_name = models.CharField(max_length=200)
    pickup_points = models.TextField(help_text="Comma-separated pickup points")
    start_time = models.TimeField()
    end_time = models.TimeField()
    distance_km = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Route {self.route_number} - {self.route_name}"

    def pickup_list(self):
        return [p.strip() for p in self.pickup_points.split(',')]


class BusPassApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    PASS_DURATION = [
        (1, '1 Month'),
        (3, '3 Months'),
        (6, '6 Months'),
        (12, '1 Year'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE)
    pickup_point = models.CharField(max_length=200)
    duration_months = models.IntegerField(choices=PASS_DURATION, default=1)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_remarks = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    valid_from = models.DateField(null=True, blank=True)
    valid_until = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.student} - Route {self.route.route_number} ({self.status})"

    def save(self, *args, **kwargs):
        self.total_fee = self.route.monthly_fee * self.duration_months
        super().save(*args, **kwargs)
