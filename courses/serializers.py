from rest_framework import serializers
from .models import Course, Enrollment

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'instructor']

class EnrollmentSerializer(serializers.ModelSerializer):

    student = serializers.StringRelatedField()  
    course = serializers.StringRelatedField()  


    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_on']
