from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.forms import FitnessAppUserCreationForm

class SignUpView(CreateView):
    form_class = FitnessAppUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"