from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from fitnessApp.models import *
from fitnessApp.forms import *

class ExerciseListView(ListView):
    model = Exercise
    template_name = "exercise_list.html"
    paginate_by = 10

class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    template_name = "exercise_create.html"
    form_class = ExerciseCreateForm

class ExerciseDetailView(LoginRequiredMixin, DetailView):
    model = Exercise
    template_name = "exercise_detail.html"