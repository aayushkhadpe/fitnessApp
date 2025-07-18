from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from fitnessApp.models import *
from fitnessApp.forms import *

class ExerciseListView(ListView):
    model = Exercise
    template_name = "exercise_list.html"
    paginate_by = 50

    def get_queryset(self):
        queryset = super().get_queryset()

        if (self.request.user.is_anonymous):
            queryset = queryset.filter(Q(public_flag="True"))
        else:
            queryset = queryset.filter(Q(creator=self.request.user.person) | Q(public_flag="True"))

        return queryset

class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    template_name = "exercise_create.html"
    form_class = ExerciseCreateForm

class ExerciseDetailView(LoginRequiredMixin, DetailView):
    model = Exercise
    template_name = "exercise_detail.html"