from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from fitnessApp.choices import *
from .workout_models import *
from .fitnessAppUser_models import *
from .exercise_models import *

class WorkoutSession(models.Model):
    workout =  models.ForeignKey(Workout, on_delete=models.CASCADE)
    user = models.ForeignKey(FitnessAppUser, on_delete=models.CASCADE)
    scheduled_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=WORKOUT_SESSION_STATUS_CHOICES, default="CREATED")
    current_step_sequence = models.IntegerField(default = 1)

class WorkoutSessionStep(models.Model):
    workoutSession = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    circuit = models.ForeignKey(WorkoutCircuit, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    circuit_exercise = models.ForeignKey(CircuitExercise, on_delete=models.CASCADE)
    set = models.IntegerField(default = 0)
    rest_after = models.IntegerField(default = 0)
    rest_before = models.IntegerField(default = 0)
    sequence_number = models.IntegerField(default = 0)
    first_flag = models.BooleanField(default=False)
    last_flag = models.BooleanField(default=False)

    class Meta:
        ordering = ['sequence_number']
