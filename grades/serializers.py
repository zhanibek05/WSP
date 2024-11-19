from rest_framework import serializers
from .models import Grade
from students.serializers import StudentSerializer
from courses.serializers import CourseSerializer

class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    teacher = serializers.StringRelatedField()

    class Meta:
        model = Grade
        fields = ['id', 'student', 'course', 'grade', 'date', 'teacher']
