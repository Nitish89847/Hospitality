from django.db import models

# Create your models here.

class Policy(models.Model):
    SCHEME_CHOICES=[
		("private",	"Private"),
		("ESI",	"ESI"),
		("PM-JAY",	"PM-JAY"),
		("state_scheme",	"State	Scheme"),
	]
    insurer	= models.CharField(max_length=255)
    scheme_type	= models.CharField(max_length=20,choices=SCHEME_CHOICES)
    sum_insured	= models.DecimalField(max_digits=12,decimal_places=2)
    room_eligibility = models.JSONField()	#	{"category":"semi-private",	"cap_per_day":	3000}
    covered_procedures = models.JSONField(default=list)  #surgery,knee replacement,heart bypass,appendectomy
    exclusions = models.JSONField(default=list)     #List all that does not covered
    co_pay_percent = models.DecimalField(max_digits=5,decimal_places=2,	default=0)    #part of bill people have to pay
    owner = models.ForeignKey("users.User",on_delete=models.CASCADE)   #owner (insurance holder)
    created_at = models.DateTimeField(auto_now_add=True)