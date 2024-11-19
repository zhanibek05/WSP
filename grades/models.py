from django.db import models
from django.conf import settings
from courses.models import Course
from students.models import Student

# Create your models here.

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    grade = models.CharField(max_length=2)
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='grades_assigned')

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student} - {self.course}: {self.grade}"
