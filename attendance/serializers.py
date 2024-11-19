# attendance/serializers.py

from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'status']
