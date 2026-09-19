from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Hospital(models.Model):
	OWNERSHIP_CHOICES = [
        ("government", "Government"),
        ("private", "Private"),
        ("trust", "Trust/Charitable"),
    ]
	name = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	latitude = models.FloatField(null=True,	blank=True)
	longitude = models.FloatField(null=True, blank=True)
	specialties	= models.JSONField(default=list)          #cardiology neurology orthopedics pediatrics obstetrics gynecology oncology ophthalmology dermatology psychiatry ENT gastroenterology nephrology pulmonology rheumatology endocrinology urology
	empanelled_schemes = models.JSONField(default=list, blank=True)			#	["PMJAY",	"ESI"]
	network_insurers = models.JSONField(default=list, blank=True)					#	insurer	names	this	hospital	accepts
	ownership_type = models.CharField(
        max_length=20, choices=OWNERSHIP_CHOICES, default="private"
    )


	def clean(self):
		if not self.empanelled_schemes and not self.network_insurers:
			raise ValidationError(
				"A hospital must have at least one empanelled scheme or one network insurer."
			)

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name

class RoomType(models.Model):
	ROOM_CATEGORY_CHOICES = [
        ("general_ward", "General Ward"),
        ("semi_private", "Semi_Private (2-bed)"),
        ("private", "Private (Single Occupancy)"),
        ("deluxe", "Deluxe/Super Deluxe"),
        ("suite", "Suite"),
        ("icu", "ICU (Intensive Care Unit)"),
        ("icu_hdu", "HDU (High Dependency Unit)"),
        ("nicu", "NICU (Neonatal ICU)"),
        ("picu", "PICU (Pediatric ICU)"),
        ("ccu", "CCU (Cardiac Care Unit)"),
        ("day_care", "Day Care (No overnight stay)"),
    ]
	hospital = models.ForeignKey(Hospital, related_name="room_types", on_delete=models.CASCADE)
	category	=	models.CharField(max_length=50, choices=ROOM_CATEGORY_CHOICES)
	indicative_cost_per_day = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
		unique_together = ("hospital", "category")

	def __str__(self):
		return f"{self.hospital.name} - {self.get_category_display()}"										#	general	|	semi-private	|	private
