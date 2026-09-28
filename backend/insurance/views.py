from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Policy
from .serializers import PolicySerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Insurer, PolicyPlan, Policy
from .serializers import InsurerSerializer, PolicyPlanSerializer, PolicySerializer

# Create your views here.

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Policy.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class InsurerListView(generics.ListAPIView):
    serializer_class = InsurerSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Insurer.objects.filter(is_active=True).order_by("name")


class PolicyPlanListView(generics.ListAPIView):
    serializer_class = PolicyPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = PolicyPlan.objects.filter(is_active=True, insurer__is_active=True)
        insurer_id = self.request.query_params.get("insurer")
        if insurer_id:
            qs = qs.filter(insurer_id=insurer_id)
        return qs.select_related("insurer")


class EnrollView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, plan_id):
        plan = get_object_or_404(PolicyPlan, id=plan_id, is_active=True)

        policy = Policy.objects.create(
            owner=request.user,
            plan=plan,
            insurer=plan.insurer.name,
            scheme_type=plan.scheme_type,
            sum_insured=plan.sum_insured,
            room_eligibility=plan.room_eligibility,
            covered_procedures=plan.covered_procedures,
            exclusions=plan.exclusions,
            co_pay_percent=plan.co_pay_percent,
        )
        return Response(PolicySerializer(policy).data, status=status.HTTP_201_CREATED)