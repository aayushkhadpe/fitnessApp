from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from datetime import date
from fitnessApp.models import *
from fitnessApp.forms import *


class SessionView(LoginRequiredMixin, ListView):
    model = WorkoutSession
    template_name = "session.html"
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()

        if (self.request.user.person.coach_flag):
            queryset = queryset.filter(Q(creator=self.request.user.person), scheduled_date=date.today()).order_by((F('scheduled_time').asc(nulls_last=True)))
        else: 
            queryset = queryset.filter(person=self.request.user.person, scheduled_date=date.today()).order_by((F('scheduled_time').asc(nulls_last=True)))

        return queryset
   
class UpcomingSessionView(LoginRequiredMixin, ListView):
    model = WorkoutSession
    template_name = "upcoming_session.html"
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()

        if (self.request.user.person.coach_flag):
            queryset = queryset.filter(Q(creator=self.request.user.person) & (Q(scheduled_date__gt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').asc(nulls_last=True)), (F('scheduled_time').asc(nulls_last=True)))
        else: 
            queryset = queryset.filter(Q(person=self.request.user.person) & (Q(scheduled_date__gt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').asc(nulls_last=True)), (F('scheduled_time').asc(nulls_last=True)))

        return queryset
          
class PastSessionView(LoginRequiredMixin, ListView):
    model = WorkoutSession
    template_name = "past_session.html"
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()

        if (self.request.user.person.coach_flag):
            queryset = queryset.filter(Q(creator=self.request.user.person) & (Q(scheduled_date__lt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').desc(nulls_last=True)), (F('scheduled_time').desc(nulls_last=True)))
        else: 
            queryset = queryset.filter(Q(person=self.request.user.person) & (Q(scheduled_date__lt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').desc(nulls_last=True)), (F('scheduled_time').desc(nulls_last=True)))

        return queryset
