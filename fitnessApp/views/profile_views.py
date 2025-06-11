from django.shortcuts import render
from django.views.generic import View, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from fitnessApp.models import *
from fitnessApp.forms import *

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = FitnessAppUser
    form_class = FitnessAppUserUpdateForm
    success_url = reverse_lazy("profile")
    template_name = "account_details.html"

class CoachDetailView(LoginRequiredMixin, DetailView):
    model = FitnessAppPerson
    template_name = "coach_detail.html"
