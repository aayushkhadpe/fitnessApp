from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from fitnessApp.choices import *

# Create your models here.

class FitnessAppUser(AbstractUser):
    dummy = models.CharField(max_length=10, blank=True)

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    video_id = models.CharField(max_length=50, blank=True)
    public_flag = models.BooleanField(default=False)
    mode =  models.CharField(max_length=20, choices=MODE_CHOICES, default="REPS")
    weight_flag = models.BooleanField(default=True)
    #TBD target muscles, equipment, user_id

    def get_absolute_url(self):
        return reverse("exercises")

class Workout(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    duration = models.IntegerField(default = 60)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVEL_CHOICES)
    target = models.CharField(max_length=20, choices=TARGET_CHOICES)
    public_flag = models.BooleanField(default=False)
    video_id = models.CharField(max_length=50, blank=True)
    #TBD target multiple, user_id

    def get_absolute_url(self):
        return reverse("workouts")

class WorkoutCircuit(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sets = models.IntegerField(default = 2)
    set_rest = models.IntegerField(default = 120)
    exercise_rest = models.IntegerField(default = 30)

    def get_absolute_url(self):
        return reverse("circuits")
    
class CircuitExercise(models.Model):
    circuit = models.ForeignKey(WorkoutCircuit, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    # number of reps or number of seconds for the exercise based on the mode of the exercise
    mode_quantity = models.IntegerField(default = 0)
    recommended_weight = models.IntegerField(default = 0, null=True)

class WorkoutSession(models.Model):
    workout =  models.ForeignKey(Workout, on_delete=models.CASCADE)
    user = models.ForeignKey(FitnessAppUser, on_delete=models.CASCADE)
    scheduled_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=WORKOUT_SESSION_STATUS_CHOICES, default="NOTSTARTED")

class WorkoutSessionStep(models.Model):
    workoutSession = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE)
    circuit = models.ForeignKey(WorkoutCircuit, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    set = models.IntegerField(default = 0)
    rest_after = models.IntegerField(default = 0)
    rest_before = models.IntegerField(default = 0)
    sequence_number = models.IntegerField(default = 0)
    first_flag = models.BooleanField(default=False)
    last_flag = models.BooleanField(default=False)

    class Meta:
        ordering = ['sequence_number']







