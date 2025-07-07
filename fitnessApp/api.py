from fitnessApp.models import *
from fitnessApp.serializers import WorkoutSessionSerializer
from rest_framework import generics

class APIWorkoutSessionDetail(generics.UpdateAPIView):
    queryset = WorkoutSession.objects.all()
    serializer_class = WorkoutSessionSerializer