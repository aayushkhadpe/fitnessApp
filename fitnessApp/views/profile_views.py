from django.shortcuts import render
from django.views.generic import View, UpdateView
from django.urls import reverse_lazy
from fitnessApp.models import *
from fitnessApp.forms import *

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')

class AccountUpdateView(UpdateView):
    model = FitnessAppUser
    form_class = FitnessAppUserUpdateForm
    success_url = reverse_lazy("profile")
    template_name = "account_details.html"
