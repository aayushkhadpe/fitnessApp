from django.forms import *
from django.contrib.auth.forms import UserCreationForm, UsernameField
from fitnessApp.models import FitnessAppUser
from fitnessApp.models.fitnessAppUser_models import FitnessAppPerson

class FitnessAppUserCreationForm(UserCreationForm):

    class Meta:
        model = FitnessAppUser
        fields = ("username", "first_name", "email")
        field_classes = {"username": UsernameField, "first_name": CharField, "email": EmailField}
        labels = {"first_name": "Name"}

    def save(self, commit=True):
        user = super().save(commit=commit)

        person = FitnessAppPerson.objects.create(first_name=user.first_name, last_name=user.last_name)
        user.person = person
        user.save()

        return user 
