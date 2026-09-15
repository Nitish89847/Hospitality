from django.db import models

# Create your models here.

class Journey(models.Model):
    patient = models.ForeignKey("users.User", on_delete=models.CASCADE)
    active_policy =	models.ForeignKey("insurance.Policy", on_delete=models.SET_NULL, null=True)
    current_stage = models.CharField(max_length=30,	default="admission")


class JourneyStageLog(models.Model):
    journey = models.ForeignKey(Journey, related_name="stage_history",	on_delete=models.CASCADE)
    stage = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)