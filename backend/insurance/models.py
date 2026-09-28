from django.db import models

# Create your models here.

from django.db import models

SCHEME_CHOICES = [
    ("private", "Private"),
    ("ESI", "ESI"),
    ("PM-JAY", "PM-JAY"),
    ("state_scheme", "State Scheme"),
]


class Insurer(models.Model):
    INSURER_TYPE_CHOICES = [
        ("private", "Private Insurer"),
        ("government", "Government Scheme"),
    ]
    # Must match the strings used in Hospital.network_insurers exactly
    name = models.CharField(max_length=255, unique=True)
    insurer_type = models.CharField(max_length=20, choices=INSURER_TYPE_CHOICES, default="private")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PolicyPlan(models.Model):
    insurer = models.ForeignKey(Insurer, related_name="plans", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    scheme_type = models.CharField(max_length=20, choices=SCHEME_CHOICES)
    sum_insured = models.DecimalField(max_digits=12, decimal_places=2)
    room_eligibility = models.JSONField()
    # {"category": "semi_private", "cap_per_day": 3000, "icu_covered": true, "icu_cap_per_day": 8000}
    covered_procedures = models.JSONField(default=list)
    exclusions = models.JSONField(default=list)
    co_pay_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("insurer", "name")

    def __str__(self):
        return f"{self.insurer.name} - {self.name}"

class Policy(models.Model):
    insurer	= models.CharField(max_length=255)
    scheme_type	= models.CharField(max_length=20,choices=SCHEME_CHOICES)
    sum_insured	= models.DecimalField(max_digits=12,decimal_places=2)
    room_eligibility = models.JSONField()
    covered_procedures = models.JSONField(default=list)  #surgery,knee replacement,heart bypass,appendectomy
    exclusions = models.JSONField(default=list)     #List all that does not covered
    co_pay_percent = models.DecimalField(max_digits=5,decimal_places=2,	default=0)    #part of bill people have to pay
    owner = models.ForeignKey("users.User",on_delete=models.CASCADE)   #owner (insurance holder)
    created_at = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(
        "insurance.PolicyPlan", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="enrollments",
    )