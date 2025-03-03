from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, DetailView
from fitnessApp.models import *
from fitnessApp.forms import *

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"
    
class ExerciseListView(ListView):
    model = Exercise
    template_name = "exercise_list.html"
    paginate_by = 10

class WorkoutListView(ListView):
    model = Workout
    template_name = "workout_list.html"
    paginate_by = 10

class ExerciseCreateView(CreateView):
    model = Exercise
    template_name = "exercise_create.html"
    form_class = ExerciseCreateForm

class WorkoutCreateView(CreateView):
    model = Workout
    template_name = "workout_create.html"
    form_class = WorkoutCreateForm

class WorkoutDetailView(DetailView):
    model = Workout
    template_name = "workout_detail.html"


    