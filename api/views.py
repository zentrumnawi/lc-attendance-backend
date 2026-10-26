from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Course, Department, Participant, Visit
from api.serializers import (
    CourseSerializer,
    DepartmentSerializer,
    ParticipantSerializer,
    VisitCreateSerializer,
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

    def get_serializer_class(self):
        if self.action == "create":
            return VisitCreateSerializer
        return VisitSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        visit = serializer.save()
        return Response(
            VisitSerializer(visit).data,
            status=status.HTTP_201_CREATED,
        )


# preemptively, in case we need it later (session-based authentication)
@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        csrf_token = request.META.get("CSRF_COOKIE")
        if not csrf_token:
            csrf_token = get_token(request)
        return Response({"csrfToken": csrf_token})
