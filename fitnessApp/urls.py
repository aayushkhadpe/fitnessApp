from django.urls import path
from fitnessApp.api import APIWorkoutSessionDetail
from fitnessApp.views import *

urlpatterns = [

    path("", HomeView.as_view(), name="home"),
    path("workouts", WorkoutListView.as_view(), name="workouts"),
    path("workouts/<int:pk>/details", WorkoutDetailView.as_view(), name="workout-detail"),

    path("exercises", ExerciseListView.as_view(), name="exercises"),
    path("exercises/<int:pk>/details", ExerciseDetailView.as_view(), name="exercise-detail"),

    path("sessions", SessionView.as_view(), name="sessions"),
    path("sessions/upcoming", UpcomingSessionView.as_view(), name="upcoming-sessions"),
    path("sessions/past", PastSessionView.as_view(), name="past-sessions"),

    path("explore", ExploreView.as_view(), name="explore"),

    path("workouts/<int:workout_id>/workoutsession/create", WorkoutSessionCreateView.as_view(), name="workoutsession-create"),

    path("build/session", WorkoutSessionBuildView.as_view(), name="build-session"),
    path("build/workout", WorkoutBuildView.as_view(), name="build-workout"),

    path("profile", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/details", AccountUpdateView.as_view(), name="account-details"),  
    path("profile/coach/<int:pk>/details", CoachDetailView.as_view(), name="coach-details"),
    path("profile/pwa-setup", PWASetupView.as_view(), name="pwa-setup"),
    path("profile/<int:pk>/delete", AccountDeleteView.as_view(), name="account-delete"),  
    
    path("clients", ClientListView.as_view(), name="clients"),
    path("clients/create", ClientCreateView.as_view(), name="client-create"),
    path("clients/<int:pk>/details", ClientUpdateView.as_view(), name="client-details"),

    path("workoutsessions/<int:pk>/do", WorkoutSessionDoView.as_view(), name="workoutsession-do"),  
    path("workoutsessions/<int:pk>/reschedule", WorkoutSessionRescheduleView.as_view(), name="workoutsession-reschedule"),  
    path("workoutsessions/<int:pk>/delete", WorkoutSessionDeleteView.as_view(), name="workoutsession-delete"),  

    # api
    path("api/workoutsessions/<int:pk>", APIWorkoutSessionDetail.as_view()),  

    # PWA manifest
    path("manifest", TemplateView.as_view(template_name="manifest.webmanifest", content_type="application/manifest+json"), name="webmanifest"),

    # Pages
    path('pages/support', SupportView.as_view(), name='pages-support'),
    path('pages/privacy-policy', TemplateView.as_view(template_name="pages/privacy_policy.html"), name='pages-privacy-policy'),
    path('pages/contactus-success', ContactUsSuccessView.as_view(), name='pages-contactus-success'),
]