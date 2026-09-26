from django.urls import path
from .views import JourneyListCreateView, AdvanceStageView

urlpatterns = [
    path("", JourneyListCreateView.as_view(), name="journey-list"),
    path("<int:journey_id>/advance/", AdvanceStageView.as_view(), name="journey-advance"),
]