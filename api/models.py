import uuid

from django.db import models


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.department.name} - {self.name}"


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    anonymousIdentifier = models.CharField(max_length=255, blank=True, default="")
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="participants",
        null=True,
        blank=True,
    )
    semester = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.anonymousIdentifier


class Visit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="visits",
    )
    startTime = models.TimeField(null=True, blank=True)
    endTime = models.TimeField(null=True, blank=True)
    date = models.DateField()
    courses = models.ManyToManyField(Course, related_name="visits", blank=True)

    def __str__(self):
        return f"{self.participant.anonymousIdentifier} - {self.date}"
