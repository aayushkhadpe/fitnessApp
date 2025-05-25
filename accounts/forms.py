from django.forms import *
from django.contrib.auth.forms import UserCreationForm, UsernameField
from fitnessApp.models import FitnessAppUser

class FitnessAppUserCreationForm(UserCreationForm):

    class Meta:
        model = FitnessAppUser
        fields = ("username", "first_name", "email")
        field_classes = {"username": UsernameField, "first_name": CharField, "email": EmailField}
        labels = {"first_name": "Name"}
