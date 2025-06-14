from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from fitnessApp.models import *
from fitnessApp.forms import *

class WorkoutSessionCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    template_name = "workoutsession_create.html"
    form_class = WorkoutSessionCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        workout_id = self.kwargs['workout_id']
        workout = Workout.objects.get(pk=workout_id)

        form.instance.workout = workout
        form.instance.person = self.request.user.person

        response = super().form_valid(form)

        seq = 1
        before = 10

        for circuit in workout.workoutcircuit_set.all():
            for setnumber in range(1, circuit.sets + 1):

                circuitexercises = circuit.circuitexercise_set.all()
                lastelement = circuitexercises.last()
                firstelement = circuitexercises.first()
                
                for circuitexercise in circuitexercises:

                    after = circuit.set_rest if circuitexercise == lastelement else circuit.exercise_rest

                    WorkoutSessionStep.objects.create(
                        workoutSession = self.object,
                        circuit = circuit,
                        exercise = circuitexercise.exercise,
                        circuit_exercise = circuitexercise,
                        set = setnumber,
                        rest_after = after,
                        rest_before = before,
                        sequence_number = seq,
                        first_flag = (circuitexercise == firstelement),
                        last_flag = (circuitexercise == lastelement),
                    )

                    seq += 1
                    before = after

        return response

class WorkoutSessionRunView(LoginRequiredMixin, DetailView):
    model = WorkoutSession
    template_name = "workoutsession_run.html"

class WorkoutSessionStepView(LoginRequiredMixin, DetailView):
    model = WorkoutSessionStep
    template_name = "workoutsession_step.html"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        # Custom lookup logic, e.g., using a different field
        workoutsession_id = self.kwargs.get('workoutsession_id')
        sequencenumber = self.kwargs.get('sequencenumber')

        obj = get_object_or_404(queryset, workoutSession=workoutsession_id, sequence_number=sequencenumber)
        obj.workoutSession.current_step_sequence = sequencenumber
        obj.workoutSession.save()
        
        return obj

class WorkoutSessionBuildView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    template_name = "workoutsession_build.html"
    form_class = WorkoutSessionBuildForm