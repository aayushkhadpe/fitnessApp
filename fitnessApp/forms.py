from django import forms
from datetime import date
from django.forms import CharField, EmailField
from django.contrib.auth.forms import UserCreationForm, UsernameField
from fitnessApp.models import Exercise, Workout, WorkoutSession, FitnessAppUser, FitnessAppPerson

class ExerciseCreateForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"

class WorkoutCreateForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = "__all__"

class ClientCreateForm(forms.ModelForm):

    class Meta:
        model = FitnessAppPerson
        fields = ("first_name", "last_name", "coach", "phone_number", "email",)

class WorkoutSessionCreateForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ["scheduled_date"]
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date', 'min': str(date.today())}, ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_date'].required = False

class FitnessAppUserUpdateForm(forms.ModelForm):

    class Meta:
        model = FitnessAppUser
        fields = ("first_name", "last_name")
        field_classes = {"first_name": CharField, "last_name": CharField}
        labels = {"first_name": "First Name", "last_name": "Last Name"}

class FitnessAppPersonUpdateForm(forms.ModelForm):
    class Meta:
        model = FitnessAppPerson
        fields = ("first_name", "last_name", "phone_number", "email")
        field_classes = {"first_name": CharField, "last_name": CharField}
        labels = {"first_name": "First Name", "last_name": "Last Name"}