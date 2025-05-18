from django.shortcuts import render
from django.views.generic import View
from fitnessApp.models import *
from fitnessApp.forms import *

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')