from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from fitnessApp.models import *
from fitnessApp.forms import *

class ClientListView(LoginRequiredMixin, ListView):
    model = FitnessAppPerson
    template_name = "client_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(coach=self.request.user.person)
        return queryset
    

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = FitnessAppPerson
    template_name = "client_create.html"
    form_class = ClientCreateForm
    

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = FitnessAppPerson
    form_class = FitnessAppPersonUpdateForm
    success_url = reverse_lazy("clients")
    template_name = "client_details.html"