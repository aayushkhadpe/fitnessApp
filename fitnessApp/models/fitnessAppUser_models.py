from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from fitnessApp.choices import *

class FitnessAppPerson(models.Model):
    first_name = models.CharField(max_length=500, null=False, blank=False)
    last_name = models.CharField(max_length=500, blank=True)
    coach_flag = models.BooleanField(default=False)
    coach = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("clients")

class FitnessAppUser(AbstractUser):
    person = models.OneToOneField(FitnessAppPerson, on_delete=models.CASCADE, null=True, related_name='person')
