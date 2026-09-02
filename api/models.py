import uuid

from django.db import models


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255, blank=True, default="")


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
