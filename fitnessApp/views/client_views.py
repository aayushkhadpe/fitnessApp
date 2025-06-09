from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from fitnessApp.models import *
from fitnessApp.forms import *

class ClientListView(LoginRequiredMixin, ListView):
    model = FitnessAppUser
    template_name = "client_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(coach=self.request.user)
        return queryset