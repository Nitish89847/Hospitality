from django.urls import path
from .views import HospitalMatchView

urlpatterns = [
    path("match/", HospitalMatchView.as_view(), name="hospital-match"),
]