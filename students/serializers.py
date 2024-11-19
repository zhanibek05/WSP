from rest_framework import serializers
from .models import Student
from courses.serializers import EnrollmentSerializer

class StudentSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'dob', 'registration_date', 'enrollments']
