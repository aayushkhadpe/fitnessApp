from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, ListView, TemplateView, DetailView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from datetime import date
from fitnessApp.models import *
from fitnessApp.forms import *

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['activeSessions'] = WorkoutSession.objects.filter(user=self.request.user, scheduled_date=date.today())
        context['upcomingSessions'] = WorkoutSession.objects.filter(Q(user=self.request.user) & (Q(scheduled_date__gt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').asc(nulls_last=True)))
        context['pastSessions'] = WorkoutSession.objects.filter(user=self.request.user, scheduled_date__lt=date.today()).order_by('-scheduled_date')

        return context
    
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

class WorkoutSessionCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    template_name = "workoutsession_create.html"
    form_class = WorkoutSessionCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        workout_id = self.kwargs['workout_id']
        workout = Workout.objects.get(pk=workout_id)

        form.instance.workout = workout
        form.instance.user = self.request.user

        return super().form_valid(form)

class ProfileView(View):
    def get(self, request):
        return render(request, 'profile.html')

    