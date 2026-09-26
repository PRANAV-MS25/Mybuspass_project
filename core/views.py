from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta
from .models import StudentProfile, BusRoute, BusPassApplication
from .forms import StudentRegistrationForm, BusPassApplicationForm, BusRouteForm


# ─── Auth Views ───────────────────────────────────────────────────────────────

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


def student_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            StudentProfile.objects.create(
                user=user,
                roll_number=form.cleaned_data['roll_number'],
                department=form.cleaned_data['department'],
                year=form.cleaned_data['year'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'core/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard' if user.is_staff else 'dashboard')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


# ─── Student Views ─────────────────────────────────────────────────────────────

@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    try:
        profile = request.user.studentprofile
    except StudentProfile.DoesNotExist:
        messages.error(request, 'Profile not found.')
        return redirect('logout')

    applications = BusPassApplication.objects.filter(student=profile)
    stats = {
        'total': applications.count(),
        'pending': applications.filter(status='pending').count(),
        'approved': applications.filter(status='approved').count(),
        'rejected': applications.filter(status='rejected').count(),
    }
    return render(request, 'core/student_dashboard.html', {
        'profile': profile,
        'applications': applications[:5],
        'stats': stats,
    })


@login_required
def apply_pass(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        form = BusPassApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.student = profile
            app.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = BusPassApplicationForm()
    routes = BusRoute.objects.filter(is_active=True)
    return render(request, 'core/apply_pass.html', {'form': form, 'routes': routes})


@login_required
def my_applications(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    profile = get_object_or_404(StudentProfile, user=request.user)
    applications = BusPassApplication.objects.filter(student=profile)
    return render(request, 'core/my_applications.html', {'applications': applications})


@login_required
def application_detail(request, pk):
    profile = get_object_or_404(StudentProfile, user=request.user)
    app = get_object_or_404(BusPassApplication, pk=pk, student=profile)
    return render(request, 'core/application_detail.html', {'app': app})


def get_route_details(request, route_id):
    route = get_object_or_404(BusRoute, pk=route_id)
    return JsonResponse({
        'pickup_points': route.pickup_list(),
        'monthly_fee': float(route.monthly_fee),
        'distance_km': float(route.distance_km),
        'start_time': route.start_time.strftime('%H:%M'),
        'end_time': route.end_time.strftime('%H:%M'),
    })


# ─── Admin Views ───────────────────────────────────────────────────────────────

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, 'Admin access required.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    stats = {
        'students': StudentProfile.objects.count(),
        'routes': BusRoute.objects.filter(is_active=True).count(),
        'pending': BusPassApplication.objects.filter(status='pending').count(),
        'approved': BusPassApplication.objects.filter(status='approved').count(),
        'rejected': BusPassApplication.objects.filter(status='rejected').count(),
        'total': BusPassApplication.objects.count(),
    }
    recent = BusPassApplication.objects.select_related('student__user', 'route').order_by('-applied_at')[:10]
    return render(request, 'core/admin_dashboard.html', {'stats': stats, 'recent': recent})


@admin_required
def admin_applications(request):
    status_filter = request.GET.get('status', '')
    apps = BusPassApplication.objects.select_related('student__user', 'route').all()
    if status_filter:
        apps = apps.filter(status=status_filter)
    return render(request, 'core/admin_applications.html', {
        'applications': apps,
        'status_filter': status_filter,
    })


@admin_required
def admin_update_status(request, pk):
    app = get_object_or_404(BusPassApplication, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        remarks = request.POST.get('remarks', '')
        if new_status in ['approved', 'rejected', 'pending']:
            app.status = new_status
            app.admin_remarks = remarks
            if new_status == 'approved':
                app.valid_from = date.today()
                app.valid_until = date.today() + timedelta(days=30 * app.duration_months)
            app.save()
            messages.success(request, f'Application {new_status} successfully.')
    return redirect('admin_applications')


@admin_required
def admin_routes(request):
    routes = BusRoute.objects.all()
    return render(request, 'core/admin_routes.html', {'routes': routes})


@admin_required
def admin_route_add(request):
    if request.method == 'POST':
        form = BusRouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route added successfully.')
            return redirect('admin_routes')
    else:
        form = BusRouteForm()
    return render(request, 'core/admin_route_form.html', {'form': form, 'action': 'Add'})


@admin_required
def admin_route_edit(request, pk):
    route = get_object_or_404(BusRoute, pk=pk)
    if request.method == 'POST':
        form = BusRouteForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            messages.success(request, 'Route updated successfully.')
            return redirect('admin_routes')
    else:
        form = BusRouteForm(instance=route)
    return render(request, 'core/admin_route_form.html', {'form': form, 'action': 'Edit', 'route': route})


@admin_required
def admin_route_delete(request, pk):
    route = get_object_or_404(BusRoute, pk=pk)
    if request.method == 'POST':
        route.delete()
        messages.success(request, 'Route deleted.')
    return redirect('admin_routes')


@admin_required
def admin_students(request):
    students = StudentProfile.objects.select_related('user').all()
    return render(request, 'core/admin_students.html', {'students': students})
