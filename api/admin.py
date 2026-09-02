from django.contrib import admin

from api.models import Course, Department, Participant, Visit


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "id")
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "id")
    list_filter = ("department",)
    search_fields = ("name",)


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("anonymousIdentifier", "department", "id")
    list_filter = ("department",)
    search_fields = ("anonymousIdentifier",)


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ("participant", "date", "startTime", "endTime", "id")
    list_filter = ("date", "participant__department")
    search_fields = ("participant__anonymousIdentifier",)
    filter_horizontal = ("courses",)
