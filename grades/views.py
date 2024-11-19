# grades/views.py

from rest_framework import viewsets
from .models import Grade
from .serializers import GradeSerializer
from users.permissions import IsAdminOrTeacher
from rest_framework.permissions import IsAuthenticated
from .tasks import send_notification_email
import logging

logger = logging.getLogger(__name__)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.select_related('student', 'course', 'teacher').all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrTeacher]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        grade = serializer.save()
        subject = f"New Grade Assigned for {grade.course.name}"
        message = (
            f"Dear {grade.student.user.first_name},\n\n"
            f"You have received a grade of {grade.grade} in {grade.course.name}.\n\n"
            f"Best Regards,\n{grade.teacher.get_full_name()}"
        )
        send_notification_email.delay(grade.student.user.email, subject, message)
        logger.info(f"Grade created and email sent to {grade.student.user.email}")
