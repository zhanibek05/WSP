from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            password='password123',
            email='student@example.com',
            first_name='Test',
            last_name='Student',
            role='student'
        )
        self.student = Student.objects.create(
            user=self.user,
            dob='2000-01-01'
        )
    
    def test_student_creation(self):
        self.assertEqual(self.student.user.username, 'teststudent')
        self.assertEqual(str(self.student), 'Test Student')
        self.assertEqual(self.student.dob.strftime('%Y-%m-%d'), '2000-01-01')
        self.assertIsNotNone(self.student.registration_date)
    
    def test_student_str(self):
        self.assertEqual(str(self.student), 'Test Student')
