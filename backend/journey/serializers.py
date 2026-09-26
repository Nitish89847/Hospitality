from rest_framework import serializers
from .models import Journey, JourneyStageLog

class JourneyStageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = JourneyStageLog
        fields = ["stage", "timestamp"]

class JourneySerializer(serializers.ModelSerializer):
    stage_history = JourneyStageLogSerializer(many=True, read_only=True)

    class Meta:
        model = Journey
        fields = ["id", "active_policy", "current_stage", "stage_history", "created_at"]