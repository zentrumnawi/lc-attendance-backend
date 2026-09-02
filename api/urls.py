from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CourseViewSet,
    DepartmentViewSet,
    ParticipantViewSet,
    VisitViewSet,
)

router = DefaultRouter()
router.register("departments", DepartmentViewSet)
router.register("courses", CourseViewSet)
router.register("participants", ParticipantViewSet)
router.register("visits", VisitViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
