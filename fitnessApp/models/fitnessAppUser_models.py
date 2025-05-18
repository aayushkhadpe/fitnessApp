from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from fitnessApp.choices import *

class FitnessAppUser(AbstractUser):
    dummy = models.CharField(max_length=10, blank=True)
