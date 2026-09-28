from django.contrib import admin
from .models import Insurer, Policy, PolicyPlan

# Register your models here.

admin.site.register(Policy)
admin.site.register(Insurer)
admin.site.register(PolicyPlan)
