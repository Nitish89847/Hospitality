from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Policy
from .serializers import PolicySerializer

# Create your views here.

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Policy.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)