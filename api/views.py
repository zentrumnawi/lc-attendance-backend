from rest_framework import viewsets

from api.models import Course, Department, Participant, Visit
from api.serializers import (
    CourseSerializer,
    DepartmentSerializer,
    ParticipantSerializer,
    VisitSerializer,
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related("department")
    serializer_class = CourseSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.select_related("department")
    serializer_class = ParticipantSerializer


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.select_related("participant").prefetch_related("courses")
    serializer_class = VisitSerializer
