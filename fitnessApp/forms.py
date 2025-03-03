from django import forms

from fitnessApp.models import Exercise, Workout

class ExerciseCreateForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"

class WorkoutCreateForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = "__all__"