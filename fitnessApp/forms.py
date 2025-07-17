from django import forms
from datetime import date
from django.forms import CharField
from fitnessApp.choices import *
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
        fields = ("first_name", "last_name", "phone_number", "email",)

    first_name = forms.CharField(label='First Name', max_length=100, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=False)
    phone_number = forms.CharField(label='Phone Number', max_length=50, required=True)
    email = forms.EmailField(label='Email', max_length=100, required=False)

    def save(self, commit=True):
        client = super().save(commit=commit)

        client.coach = self.user.person
        client.save()

        return client

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

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

    first_name = forms.CharField(label='First Name', max_length=100, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=False)
    phone_number = forms.CharField(label='Phone Number', max_length=50, required=True)
    email = forms.EmailField(label='Email', max_length=100, required=False)

class WorkoutSessionRescheduleForm(forms.ModelForm):

    class Meta:
        model = WorkoutSession
        fields = ("scheduled_date", "scheduled_time")

    scheduled_date = forms.DateField(required=True)
    scheduled_time = forms.TimeField(required=True)
    
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

class BaseBuildForm(forms.Form):

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
                self.fields[f'exercise_rest_{circuitIndex + 1}_{exerciseIndex + 1}'] = forms.IntegerField()
                self.fields[f'exercise_mode_{circuitIndex + 1}_{exerciseIndex + 1}'] = forms.ChoiceField(choices=MODE_CHOICES,  widget=forms.RadioSelect(), initial=1)

class WorkoutSessionBuildForm(BaseBuildForm):

    session_client = forms.ChoiceField()
    session_date = forms.DateField()
    session_time = forms.TimeField()

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if (user.person.coach_flag == True):
            clients = FitnessAppPerson.objects.filter(coach=user.person).order_by('first_name')
            self.fields['session_client'].choices = [("", "Select a client...")] + [(client.id, (client.first_name + " " + client.last_name)) for client in clients]
        else:
            self.fields['session_client'].required = False

class WorkoutBuildForm(BaseBuildForm):

    workout_name = forms.CharField(required = True, max_length=200)
    workout_duration = forms.IntegerField(required = True, min_value=5, max_value=240, initial=60)
    workout_target = forms.ChoiceField(required = True, choices=TARGET_CHOICES)
    workout_difficulty_level = forms.ChoiceField(required = True, choices=DIFFICULTY_LEVEL_CHOICES)

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

class WorkoutSessionCreateForm(forms.ModelForm):

    class Meta:
        model = WorkoutSession
        fields = ('person_id', 'scheduled_date', 'scheduled_time', )

    person_id = forms.ChoiceField()
    scheduled_date = forms.DateField()
    scheduled_time = forms.TimeField()

    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        clients = FitnessAppPerson.objects.filter(coach=user.person).order_by('first_name')
        self.fields['person_id'].choices = [("", "Select a client...")] + [(client.id, (client.first_name + " " + client.last_name)) for client in clients]