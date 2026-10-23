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

    def get_queryset(self):
        queryset = super().get_queryset()
        anonymous_identifier = self.request.query_params.get("anonymousIdentifier")
        if anonymous_identifier is not None:
            queryset = queryset.filter(anonymousIdentifier=anonymous_identifier)
        return queryset


class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.select_related("participant").prefetch_related("courses")
    serializer_class = VisitSerializer
