from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Hospital(models.Model):
	name = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	latitude = models.FloatField(null=True,	blank=True)
	longitude = models.FloatField(null=True, blank=True)
	specialties	= models.JSONField(default=list)          #cardiology neurology orthopedics pediatrics obstetrics gynecology oncology ophthalmology dermatology psychiatry ENT gastroenterology nephrology pulmonology rheumatology endocrinology urology
	empanelled_schemes = models.JSONField(default=list,null=True, blank=True)			#	["PMJAY",	"ESI"]
	network_insurers = models.JSONField(default=list,null=True, blank=True)					#	insurer	names	this	hospital	accepts


	def clean(self):
		if not self.empanelled_schemes and not self.network_insurers:
			raise ValidationError(
				"A hospital must have at least one empanelled scheme or one network insurer."
			)

class RoomType(models.Model):
	hospital = models.ForeignKey(Hospital, related_name="room_types", on_delete=models.CASCADE)
	category	=	models.CharField(max_length=50)
	indicative_cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)											#	general	|	semi-private	|	private
