# StudentManagementSystem/urls.py

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),             # Djoser authentication endpoints
    path('api/auth/', include('djoser.urls.jwt')),         # JWT authentication endpoints
    path('api/users/', include('users.urls')),             # Users app endpoints (if any)
    path('api/students/', include('students.urls')),       # Students app endpoints
    path('api/courses/', include('courses.urls')),         # Courses app endpoints
    path('api/grades/', include('grades.urls')),           # Grades app endpoints
    path('api/attendance/', include('attendance.urls')),   # Attendance app endpoints
    path('api/notifications/', include('notifications.urls')),  # Notifications app endpoints

    # drf-spectacular endpoints
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Swagger UI with AllowAny
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(
        url_name='schema',
        permission_classes=[permissions.AllowAny],  # Temporarily set to AllowAny
    ), name='swagger-ui'),
    # ReDoc UI with AllowAny
    path('api/docs/redoc/', SpectacularRedocView.as_view(
        url_name='schema',
        permission_classes=[permissions.AllowAny],  # Temporarily set to AllowAny
    ), name='redoc'),
]
