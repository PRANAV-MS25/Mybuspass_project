from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.student_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Student
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('apply/', views.apply_pass, name='apply_pass'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),
    path('api/route/<int:route_id>/', views.get_route_details, name='route_details'),

    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/applications/', views.admin_applications, name='admin_applications'),
    path('admin-panel/applications/<int:pk>/update/', views.admin_update_status, name='admin_update_status'),
    path('admin-panel/routes/', views.admin_routes, name='admin_routes'),
    path('admin-panel/routes/add/', views.admin_route_add, name='admin_route_add'),
    path('admin-panel/routes/<int:pk>/edit/', views.admin_route_edit, name='admin_route_edit'),
    path('admin-panel/routes/<int:pk>/delete/', views.admin_route_delete, name='admin_route_delete'),
    path('admin-panel/students/', views.admin_students, name='admin_students'),
]
