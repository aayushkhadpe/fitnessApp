from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, DetailView
from fitnessApp.models import *
from fitnessApp.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"
    
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

    