from django.db import models
from django.utils import timezone

# Create your models here.

class Journey(models.Model):
    STAGE_CHOICES = [
        ("admission", "Admission"),
        ("investigation", "Investigation"),
        ("procedure", "Procedure"),
        ("recovery", "Recovery"),
        ("discharge", "Discharge"),
    ]
    patient = models.ForeignKey("users.User", on_delete=models.CASCADE)
    active_policy =	models.ForeignKey("insurance.Policy", on_delete=models.SET_NULL, null=True)
    current_stage = models.CharField(max_length=30, choices=STAGE_CHOICES, default="admission")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Journey for {self.patient.username} - {self.current_stage}"


class JourneyStageLog(models.Model):
    journey = models.ForeignKey(Journey, related_name="stage_history",	on_delete=models.CASCADE)
    stage = models.CharField(max_length=30)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.journey} -> {self.stage} at {self.timestamp}"