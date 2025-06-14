from django.urls import path
from fitnessApp.views import *

urlpatterns = [

    path("", HomeView.as_view(), name="home"),
    path("workouts", WorkoutListView.as_view(), name="workouts"),
    path("workouts/create", WorkoutCreateView.as_view(), name="workout-create"),
    path("workouts/<int:pk>/details", WorkoutDetailView.as_view(), name="workout-detail"),

    path("exercises", ExerciseListView.as_view(), name="exercises"),
    path("exercises/create", ExerciseCreateView.as_view(), name="exercise-create"),
    path("exercises/<int:pk>/details", ExerciseDetailView.as_view(), name="exercise-detail"),

    path("workouts/<int:workout_id>/workoutsession/create", WorkoutSessionCreateView.as_view(), name="workoutsession-create"),

    path("workoutsessions/<int:pk>/run", WorkoutSessionRunView.as_view(), name="workoutsession-run"),  
    path("workoutsessions/<int:workoutsession_id>/run/<int:sequencenumber>", WorkoutSessionStepView.as_view(), name="workoutsession-step"),  
    path("workoutsessions/build", WorkoutSessionBuildView.as_view(), name="workoutsession-build"),

    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/details", AccountUpdateView.as_view(), name="account-details"),  
    path("profile/coach/<int:pk>/details", CoachDetailView.as_view(), name="coach-details"),
    
    path("clients", ClientListView.as_view(), name="clients"),
    path("clients/create", ClientCreateView.as_view(), name="client-create"),
    path("clients/<int:pk>/details", ClientUpdateView.as_view(), name="client-details"),

]