from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from fitnessApp.models import *
from fitnessApp.forms import *

class WorkoutListView(ListView):
    model = Workout
    template_name = "workout_list.html"
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter((Q(creator=self.request.user.person) | Q(public_flag="True")) & Q(personalized_flag="False"))
        return queryset

class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    template_name = "workout_create.html"
    form_class = WorkoutCreateForm

class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = "workout_detail.html"