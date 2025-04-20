from django import forms
from datetime import date
from fitnessApp.models import Exercise, Workout, WorkoutSession

class ExerciseCreateForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"

class WorkoutCreateForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = "__all__"

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