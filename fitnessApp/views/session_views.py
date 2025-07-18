from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from datetime import date
from fitnessApp.models import *
from fitnessApp.forms import *


class SessionView(LoginRequiredMixin, TemplateView):
    template_name = "session.html"
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if (self.request.user.is_authenticated):
            context['today'] = date.today()
            if (self.request.user.person.coach_flag):
                context['activeSessions'] = WorkoutSession.objects.filter(Q(creator=self.request.user.person), scheduled_date=date.today()).order_by((F('scheduled_time').asc(nulls_last=True)))
            else: 
                context['activeSessions'] = WorkoutSession.objects.filter(person=self.request.user.person, scheduled_date=date.today()).order_by((F('scheduled_time').asc(nulls_last=True)))

        return context
    
class UpcomingSessionView(LoginRequiredMixin, TemplateView):
    template_name = "upcoming_session.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if (self.request.user.is_authenticated):
            context['today'] = date.today()
            if (self.request.user.person.coach_flag):
                context['upcomingSessions'] = WorkoutSession.objects.filter(Q(creator=self.request.user.person) & (Q(scheduled_date__gt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').asc(nulls_last=True)), (F('scheduled_time').asc(nulls_last=True)))
            else: 
                context['upcomingSessions'] = WorkoutSession.objects.filter(Q(person=self.request.user.person) & (Q(scheduled_date__gt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').asc(nulls_last=True)), (F('scheduled_time').asc(nulls_last=True)))

        return context

class PastSessionView(LoginRequiredMixin, TemplateView):
    template_name = "past_session.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if (self.request.user.is_authenticated):
            context['today'] = date.today()
            if (self.request.user.person.coach_flag):
                context['pastSessions'] = WorkoutSession.objects.filter(Q(creator=self.request.user.person) & (Q(scheduled_date__lt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').desc(nulls_last=True)), (F('scheduled_time').desc(nulls_last=True)))
            else: 
                context['pastSessions'] = WorkoutSession.objects.filter(Q(person=self.request.user.person) & (Q(scheduled_date__lt=date.today()) | Q(scheduled_date__isnull=True))).order_by((F('scheduled_date').desc(nulls_last=True)), (F('scheduled_time').desc(nulls_last=True)))

        return context