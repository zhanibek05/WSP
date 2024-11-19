from django.conf import settings
from django.db import models

# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    dob = models.DateField()
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()