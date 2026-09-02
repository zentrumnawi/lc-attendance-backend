from rest_framework import serializers

from api.models import Course, Department, Participant, Visit


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "department", "name"]


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ["id", "anonymousIdentifier", "department", "semester"]


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = [
            "id",
            "participant",
            "startTime",
            "endTime",
            "date",
            "courses",
        ]
