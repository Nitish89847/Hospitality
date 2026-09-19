from rest_framework import serializers
from .models import Hospital, RoomType

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ["id", "category", "indicative_cost_per_day"]

class HospitalSerializer(serializers.ModelSerializer):
    room_types = RoomTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Hospital
        fields = ["id", "name", "city", "specialties", "empanelled_schemes", "ownership_type", "network_insurers", "room_types"]