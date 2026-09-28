from rest_framework.routers import DefaultRouter
from .views import PolicyViewSet
from django.urls import path
from .views import PolicyViewSet, InsurerListView, PolicyPlanListView, EnrollView

router = DefaultRouter()
router.register(r"policies", PolicyViewSet, basename="policy")

urlpatterns = router.urls + [
    path("insurers/", InsurerListView.as_view(), name="insurer-list"),
    path("plans/", PolicyPlanListView.as_view(), name="plan-list"),
    path("plans/<int:plan_id>/enroll/", EnrollView.as_view(), name="plan-enroll"),
]