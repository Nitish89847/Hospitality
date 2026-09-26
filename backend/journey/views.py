from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Journey, JourneyStageLog
from .serializers import JourneySerializer

# Create your views here.
class JourneyListCreateView(generics.ListCreateAPIView):
    serializer_class = JourneySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Journey.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)


class AdvanceStageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, journey_id):
        journey = Journey.objects.get(id=journey_id, patient=request.user)
        stages = [s[0] for s in Journey.STAGE_CHOICES]
        current_index = stages.index(journey.current_stage)

        if current_index + 1 < len(stages):
            journey.current_stage = stages[current_index + 1]
            journey.save()
            JourneyStageLog.objects.create(journey=journey, stage=journey.current_stage)

        return Response(JourneySerializer(journey).data)
