from django.db import models
from django.urls import reverse
from fitnessApp.choices import *

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    video_id = models.CharField(max_length=50, null=True)
    public_flag = models.BooleanField(default=False)
    mode =  models.CharField(max_length=20, choices=MODE_CHOICES, default="REPS")
    weight_flag = models.BooleanField(default=True)
    #TBD target muscles, equipment, user_id

    def get_absolute_url(self):
        return reverse("exercises")