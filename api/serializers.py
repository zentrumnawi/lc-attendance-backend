from rest_framework import serializers

from api.models import Course, Department, Participant, Visit


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "department", "name", "department_name"]


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


class VisitCreateSerializer(serializers.Serializer):
    anonymousIdentifier = serializers.CharField(max_length=255)
    semester = serializers.IntegerField(required=False, allow_null=True)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        allow_null=True,
    )
    startTime = serializers.TimeField(required=False, allow_null=True)
    endTime = serializers.TimeField(required=False, allow_null=True)
    date = serializers.DateField()
    courses = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        many=True,
        required=False,
    )

    def create(self, validated_data):
        courses = validated_data.pop("courses", [])
        anonymous_identifier = validated_data.pop("anonymousIdentifier")
        semester = validated_data.pop("semester", None)
        department = validated_data.pop("department", None)

        participant, _ = Participant.objects.update_or_create(
            anonymousIdentifier=anonymous_identifier,
            defaults={
                "semester": semester,
                "department": department,
            },
        )

        visit = Visit.objects.create(
            participant=participant,
            startTime=validated_data.get("startTime"),
            endTime=validated_data.get("endTime"),
            date=validated_data["date"],
        )
        if courses:
            visit.courses.set(courses)
        return visit
