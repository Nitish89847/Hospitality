from rest_framework import serializers
from .models import Policy, Insurer, PolicyPlan

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

class InsurerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurer
        fields = ["id", "name", "insurer_type"]


class PolicyPlanSerializer(serializers.ModelSerializer):
    insurer_name = serializers.CharField(source="insurer.name", read_only=True)

    class Meta:
        model = PolicyPlan
        fields = [
            "id", "plan", "insurer", "insurer_name", "name", "scheme_type",
            "sum_insured", "room_eligibility", "covered_procedures",
            "exclusions", "co_pay_percent",
        ]