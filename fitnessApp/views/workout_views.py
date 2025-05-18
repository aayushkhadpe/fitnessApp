from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from fitnessApp.models import *
from fitnessApp.forms import *

class WorkoutListView(ListView):
    model = Workout
    template_name = "workout_list.html"
    paginate_by = 10

class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    template_name = "workout_create.html"
    form_class = WorkoutCreateForm

class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = "workout_detail.html"