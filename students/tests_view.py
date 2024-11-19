# students/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

class StudentViewSetTest(APITestCase):
    def setUp(self):
        # Create users with different roles
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            email='admin@example.com',
            role='admin'
        )
        self.teacher_user = User.objects.create_user(
            username='teacher',
            password='teacherpass',
            email='teacher@example.com',
            role='teacher'
        )
        self.student_user = User.objects.create_user(
            username='student',
            password='studentpass',
            email='student@example.com',
            role='student'
        )
        
        # Create a Student instance
        self.student = Student.objects.create(
            user=self.student_user,
            dob='2000-01-01'
        )
        
        # API endpoints
        self.list_url = reverse('student-list')  # Assuming basename='student'
        self.detail_url = reverse('student-detail', kwargs={'pk': self.student.pk})
    
    def authenticate(self, user):
        self.client.force_authenticate(user=user)
    
    def test_admin_can_create_student(self):
        self.authenticate(self.admin_user)
        data = {
            'user': {
                'username': 'newstudent',
                'password': 'newpass123',
                'email': 'newstudent@example.com',
                'first_name': 'New',
                'last_name': 'Student',
                'role': 'student'
            },
            'dob': '1999-12-31'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(Student.objects.get(pk=response.data['id']).user.username, 'newstudent')
    
    def test_teacher_cannot_create_student(self):
        self.authenticate(self.teacher_user)
        data = {
            'user': {
                'username': 'unauthorizedstudent',
                'password': 'pass1234',
                'email': 'unauthstudent@example.com',
                'first_name': 'Unauthorized',
                'last_name': 'Student',
                'role': 'student'
            },
            'dob': '1998-11-30'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_student_can_view_own_profile(self):
        self.authenticate(self.student_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'student')
    
    def test_student_cannot_view_other_profiles(self):
        # Create another student
        other_user = User.objects.create_user(
            username='otherstudent',
            password='otherpass123',
            email='otherstudent@example.com',
            role='student'
        )
        other_student = Student.objects.create(
            user=other_user,
            dob='1999-05-15'
        )
        self.authenticate(self.student_user)
        other_detail_url = reverse('student-detail', kwargs={'pk': other_student.pk})
        response = self.client.get(other_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_admin_can_update_student(self):
        self.authenticate(self.admin_user)
        data = {
            'dob': '2001-02-02'
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.dob.strftime('%Y-%m-%d'), '2001-02-02')
    
    def test_teacher_can_update_student(self):
        self.authenticate(self.teacher_user)
        data = {
            'dob': '2002-03-03'
        }
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Assuming teachers cannot update student profiles
    
    def test_admin_can_delete_student(self):
        self.authenticate(self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
    
    def test_teacher_cannot_delete_student(self):
        self.authenticate(self.teacher_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_caching_student_list(self):
        # Assuming caching is implemented for the student list
        self.authenticate(self.admin_user)
        response1 = self.client.get(self.list_url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Modify the database
        new_user = User.objects.create_user(
            username='cachedstudent',
            password='cachepass123',
            email='cachedstudent@example.com',
            role='student'
        )
        Student.objects.create(
            user=new_user,
            dob='2003-04-04'
        )
        
        # Fetch the list again; should be cached, hence count remains the same
        response2 = self.client.get(self.list_url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['results']), len(response1.data['results']))
    
    def test_cache_invalidation_on_create(self):
        # Assuming cache invalidates on create
        self.authenticate(self.admin_user)
        response1 = self.client.get(self.list_url)
        initial_count = len(response1.data['results'])
        
        # Create a new student
        data = {
            'user': {
                'username': 'newstudent2',
                'password': 'newpass456',
                'email': 'newstudent2@example.com',
                'first_name': 'New2',
                'last_name': 'Student2',
                'role': 'student'
            },
            'dob': '2004-05-05'
        }
        response_create = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        
        # Fetch the list again; cache should invalidate, count increases
        response2 = self.client.get(self.list_url)
        self.assertEqual(len(response2.data['results']), initial_count + 1)
