from django.urls import path

from fitnessApp.views import *

urlpatterns = [

    path("home", HomeView.as_view(), name="home"),

    path("workouts", WorkoutListView.as_view(), name="workouts"),
    path("workouts/create", WorkoutCreateView.as_view(), name="workout-create"),

    path("exercises", ExerciseListView.as_view(), name="exercises"),
    path("exercises/create", ExerciseCreateView.as_view(), name="exercise-create"),

]