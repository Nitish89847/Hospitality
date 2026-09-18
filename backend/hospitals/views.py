from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from insurance.models import Policy
from .models import Hospital
from .serializers import HospitalSerializer

# Create your views here.

class HospitalMatchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        policy_id = request.query_params.get("policy_id")
        policy = Policy.objects.get(id=policy_id, owner=request.user)

        matches = Hospital.objects.filter(network_insurers__contains=[policy.insurer])
        return Response(HospitalSerializer(matches, many=True).data)