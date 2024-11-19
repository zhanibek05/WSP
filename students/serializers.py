
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):

    enrollments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
   
    class Meta:
        model = Student
        fields = ['id', 'user', 'dob', 'registration_date', 'enrollments']
