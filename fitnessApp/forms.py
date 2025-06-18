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

CLIENTS = [
    ('', 'Select a client...'),
    ('1', 'Bhushan Khadpe'),
    ('2', 'Aayush Khadpe'),
    ('3', 'John Doe'),
]

SETS = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]

class WorkoutSessionBuildForm(forms.Form):

    session_client = forms.ChoiceField(choices=CLIENTS, initial=1)
    session_date = forms.DateField()
    session_time = forms.TimeField()

    number_of_circuits = forms.ChoiceField(choices=SETS,  widget=forms.RadioSelect(), initial=1)
    circuit_sets = forms.ChoiceField(choices=SETS,  widget=forms.RadioSelect(), initial=3)

    set_rest = forms.IntegerField()
    exercise_rest = forms.IntegerField()

    exercise_mode = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_reps = forms.IntegerField()
    exercise_time = forms.IntegerField()

    exercises_1 = forms.CharField()
    exercises_2 = forms.CharField()
    exercises_3 = forms.CharField()
    exercises_4 = forms.CharField()
    exercises_5 = forms.CharField()

    exercise_mode_1_1 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_2 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_3 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_4 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_5 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_6 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_7 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_8 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_9 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_10 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_11 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_12 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_13 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_14 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_1_15 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_1 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_2 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_3 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_4 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_5 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_6 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_7 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_8 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_9 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_10 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_11 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_12 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_13 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_14 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_2_15 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_1 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_2 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_3 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_4 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_5 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_6 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_7 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_8 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_9 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_10 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_11 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_12 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_13 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_14 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_3_15 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_1 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_2 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_3 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_4 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_5 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_6 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_7 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_8 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_9 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_10 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_11 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_12 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_13 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_14 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_4_15 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_1 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_2 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_3 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_4 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_5 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_6 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_7 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_8 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_9 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_10 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_11 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_12 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_13 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_14 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)
    exercise_mode_5_15 = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)

    exercise_quantity_1_1 = forms.IntegerField()
    exercise_quantity_1_2 = forms.IntegerField()
    exercise_quantity_1_3 = forms.IntegerField()
    exercise_quantity_1_4 = forms.IntegerField()
    exercise_quantity_1_5 = forms.IntegerField()
    exercise_quantity_1_6 = forms.IntegerField()
    exercise_quantity_1_7 = forms.IntegerField()
    exercise_quantity_1_8 = forms.IntegerField()
    exercise_quantity_1_9 = forms.IntegerField()
    exercise_quantity_1_10 = forms.IntegerField()
    exercise_quantity_1_11 = forms.IntegerField()
    exercise_quantity_1_12 = forms.IntegerField()
    exercise_quantity_1_13 = forms.IntegerField()
    exercise_quantity_1_14 = forms.IntegerField()
    exercise_quantity_1_15 = forms.IntegerField()
    exercise_quantity_2_1 = forms.IntegerField()
    exercise_quantity_2_2 = forms.IntegerField()
    exercise_quantity_2_3 = forms.IntegerField()
    exercise_quantity_2_4 = forms.IntegerField()
    exercise_quantity_2_5 = forms.IntegerField()
    exercise_quantity_2_6 = forms.IntegerField()
    exercise_quantity_2_7 = forms.IntegerField()
    exercise_quantity_2_8 = forms.IntegerField()
    exercise_quantity_2_9 = forms.IntegerField()
    exercise_quantity_2_10 = forms.IntegerField()
    exercise_quantity_2_11 = forms.IntegerField()
    exercise_quantity_2_12 = forms.IntegerField()
    exercise_quantity_2_13 = forms.IntegerField()
    exercise_quantity_2_14 = forms.IntegerField()
    exercise_quantity_2_15 = forms.IntegerField()
    exercise_quantity_3_1 = forms.IntegerField()
    exercise_quantity_3_2 = forms.IntegerField()
    exercise_quantity_3_3 = forms.IntegerField()
    exercise_quantity_3_4 = forms.IntegerField()
    exercise_quantity_3_5 = forms.IntegerField()
    exercise_quantity_3_6 = forms.IntegerField()
    exercise_quantity_3_7 = forms.IntegerField()
    exercise_quantity_3_8 = forms.IntegerField()
    exercise_quantity_3_9 = forms.IntegerField()
    exercise_quantity_3_10 = forms.IntegerField()
    exercise_quantity_3_11 = forms.IntegerField()
    exercise_quantity_3_12 = forms.IntegerField()
    exercise_quantity_3_13 = forms.IntegerField()
    exercise_quantity_3_14 = forms.IntegerField()
    exercise_quantity_3_15 = forms.IntegerField()
    exercise_quantity_4_1 = forms.IntegerField()
    exercise_quantity_4_2 = forms.IntegerField()
    exercise_quantity_4_3 = forms.IntegerField()
    exercise_quantity_4_4 = forms.IntegerField()
    exercise_quantity_4_5 = forms.IntegerField()
    exercise_quantity_4_6 = forms.IntegerField()
    exercise_quantity_4_7 = forms.IntegerField()
    exercise_quantity_4_8 = forms.IntegerField()
    exercise_quantity_4_9 = forms.IntegerField()
    exercise_quantity_4_10 = forms.IntegerField()
    exercise_quantity_4_11 = forms.IntegerField()
    exercise_quantity_4_12 = forms.IntegerField()
    exercise_quantity_4_13 = forms.IntegerField()
    exercise_quantity_4_14 = forms.IntegerField()
    exercise_quantity_4_15 = forms.IntegerField()
    exercise_quantity_5_1 = forms.IntegerField()
    exercise_quantity_5_2 = forms.IntegerField()
    exercise_quantity_5_3 = forms.IntegerField()
    exercise_quantity_5_4 = forms.IntegerField()
    exercise_quantity_5_5 = forms.IntegerField()
    exercise_quantity_5_6 = forms.IntegerField()
    exercise_quantity_5_7 = forms.IntegerField()
    exercise_quantity_5_8 = forms.IntegerField()
    exercise_quantity_5_9 = forms.IntegerField()
    exercise_quantity_5_10 = forms.IntegerField()
    exercise_quantity_5_11 = forms.IntegerField()
    exercise_quantity_5_12 = forms.IntegerField()
    exercise_quantity_5_13 = forms.IntegerField()
    exercise_quantity_5_14 = forms.IntegerField()
    exercise_quantity_5_15 = forms.IntegerField()
        