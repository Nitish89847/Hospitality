from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from insurance.models import Policy
from .models import Hospital
from .serializers import HospitalSerializer
from .services.eligibility_engine import compute_room_coverage

# Create your views here.

class HospitalMatchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        policy_id = request.query_params.get("policy_id")
        policy = Policy.objects.get(id=policy_id, owner=request.user)

        if policy.scheme_type == "private":
            hospitals = Hospital.objects.filter(network_insurers__contains=[policy.insurer])
        else:
            hospitals = Hospital.objects.filter(empanelled_schemes__contains=[policy.scheme_type])

        result = []
        for hospital in hospitals:
            hospital_data = HospitalSerializer(hospital).data
            room_lookup = {room.id: room for room in hospital.room_types.all()}
            for room in hospital_data["room_types"]:
                room_obj = room_lookup.get(room["id"])
                room.update(compute_room_coverage(policy, room_obj))
            result.append(hospital_data)

        return Response(result)