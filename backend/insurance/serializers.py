from rest_framework import serializers
from .models import Policy

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = [
            "id",
            "insurer",
            "scheme_type",
            "sum_insured",
            "room_eligibility",
            "covered_procedures",
            "exclusions",
            "co_pay_percent",
            "owner",
            "created_at",
        ]
        read_only_fields = ["id", "owner", "created_at"]