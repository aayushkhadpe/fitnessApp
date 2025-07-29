from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from fitnessApp.models import FitnessAppUser
from fitnessApp.models.fitnessAppUser_models import FitnessAppPerson

class FitnessAppUserCreationForm(UserCreationForm):

    class Meta:
        model = FitnessAppUser
        fields = ("email",)

        email = forms.EmailField(label='Email', max_length=100, required=False)

    first_name = forms.CharField(label='First Name', max_length=50, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=False)
    phone_number = forms.CharField(label='Phone Number', max_length=20, required=False)
    request_coach = forms.BooleanField(label='Request trainer account', required=False, initial=False)
    field_order = ['email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'request_coach']


    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)

        person = FitnessAppPerson.objects.create(first_name=self.cleaned_data['first_name'],
                                                 last_name=self.cleaned_data['last_name'],
                                                 phone_number=self.cleaned_data['phone_number'],
                                                 email=self.cleaned_data['email'],
                                                 coach_flag=self.cleaned_data['request_coach'])
        user.person = person
        user.save()

        return user 