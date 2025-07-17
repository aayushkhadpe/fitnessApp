from django.db import models
from django.urls import reverse
from fitnessApp.choices import *
from fitnessApp.models.fitnessAppUser_models import FitnessAppPerson

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    video_id = models.CharField(max_length=50, null=True)
    public_flag = models.BooleanField(default=False)
    weight_flag = models.BooleanField(default=True)
    creator = models.ForeignKey(FitnessAppPerson, on_delete=models.SET_NULL, null=True)
    #TBD target muscles, equipment, user_id

    def get_absolute_url(self):
        return reverse("exercises")