from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ("patient", "Patient"),
        ("caregiver", "Caregiver"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # links a caregiver to the patient(s) they manage
    managed_patients = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="caregivers",
        blank=True,
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
