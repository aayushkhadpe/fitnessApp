from django.db import models
from django.urls import reverse
from fitnessApp.choices import *

# Create your models here.

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




