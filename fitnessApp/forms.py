from django import forms
from datetime import date
from django.forms import CharField, EmailField
from django.contrib.auth.forms import UserCreationForm, UsernameField
from fitnessApp.choices import MODE_CHOICES
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

SETS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

CIRCUITS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

class WorkoutSessionBuildForm(forms.Form):

    session_client = forms.ChoiceField()
    session_date = forms.DateField()
    session_time = forms.TimeField()

    number_of_circuits = forms.ChoiceField(choices=CIRCUITS,  widget=forms.RadioSelect(), initial=1)
    circuit_sets = forms.ChoiceField(choices=SETS,  widget=forms.RadioSelect(), initial=3)

    set_rest = forms.IntegerField()
    exercise_rest = forms.IntegerField()

    exercise_mode = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_reps = forms.IntegerField()
    exercise_time = forms.IntegerField()

    exercises_1 = forms.CharField(required = False)
    exercises_2 = forms.CharField(required = False)
    exercises_3 = forms.CharField(required = False)
    exercises_4 = forms.CharField(required = False)
    exercises_5 = forms.CharField(required = False)

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        for circuitIndex in range (0, 5):
            for exerciseIndex in range (0, 15):
                self.fields[f'exercise_quantity_{circuitIndex + 1}_{exerciseIndex + 1}'] = forms.IntegerField()
                self.fields[f'exercise_mode_{circuitIndex + 1}_{exerciseIndex + 1}'] = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)

        clients = FitnessAppPerson.objects.filter(coach=user.person).order_by('first_name')
        self.fields['session_client'].choices = [("", "Select a client...")] + [(client.id, (client.first_name + " " + client.last_name)) for client in clients]
