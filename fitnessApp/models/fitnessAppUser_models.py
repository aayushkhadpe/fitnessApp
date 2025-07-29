from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from fitnessApp.managers import FitnessAppUserManager


from fitnessApp.choices import *

class FitnessAppPerson(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=100, blank=True)
    coach_flag = models.BooleanField(default=False)
    coach = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    request_coach_flag = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse("clients")

class FitnessAppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True, error_messages={'unique': "This email address is already registered. Please use a different one."})
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    person = models.OneToOneField(FitnessAppPerson, on_delete=models.CASCADE, null=True, related_name='person')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = FitnessAppUserManager()

    def __str__(self):
        return self.email