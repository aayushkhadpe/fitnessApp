from rest_framework import serializers
from fitnessApp.models.workoutSession_models import WorkoutSession

class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'