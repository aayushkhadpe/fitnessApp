from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView
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


class WorkoutSessionBuildView(FormView):
       template_name = 'workoutsession_build.html'
       form_class = WorkoutSessionBuildForm
       success_url = reverse_lazy("home")
       
       def form_valid(self, form):
           # Process the valid form data here

           set_rest = form.cleaned_data['set_rest']
           exercise_rest = form.cleaned_data['exercise_rest']
           session_client = form.cleaned_data['session_client']
           session_date = form.cleaned_data['session_date']
           session_time = form.cleaned_data['session_time']
        #    exercises = form.cleaned_data['exercises']
           exercise_reps = form.cleaned_data['exercise_reps']
           exercise_time = form.cleaned_data['exercise_time']

           # Redirect to the success URL
           return super().form_valid(form)
        
       def form_invalid(self, form):
           # Handle invalid form data
           return super().form_invalid(form)