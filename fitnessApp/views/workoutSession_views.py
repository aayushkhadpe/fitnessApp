import json
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from fitnessApp.data import *
from fitnessApp.models import *
from fitnessApp.forms import *
from fitnessApp.services import *

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

        create_workout_session_steps(self.object)

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
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exercises = Exercise.objects.all().values('id', 'name')
        exercises_json = json.dumps(list(exercises))
        context['num_circuit_exercises'] = range(15)
        context['exercises_json'] = exercises_json

        return context

    def form_valid(self, form):
        # Process the valid form data here

        session_info = SessionInfo(client_id = int(form.cleaned_data['session_client']), 
                                    scheduled_date = form.cleaned_data['session_date'],
                                    scheduled_time = form.cleaned_data['session_time'])
        
        workout_info = self.create_workout_info(form)
        # workout_info.name = "Workout @ " + str(session_info.scheduled_date)
        client = FitnessAppPerson.objects.get(pk=session_info.client_id)
        workout_info.name = self.request.user.person.first_name + " - " + client.first_name + " - " + str(session_info.scheduled_date)

        create_workout_session(session_info, workout_info)

        # Redirect to the success URL
        return super().form_valid(form)
   
    def form_invalid(self, form):
        # Handle invalid form data
        return super().form_invalid(form)

    def create_workout_info(self, form):
        
        # create workout info
        workout_info = WorkoutInfo( name = "",
                                    num_circuits = int(form.cleaned_data['number_of_circuits']),
                                    num_sets = int(form.cleaned_data['circuit_sets']),
                                    set_rest = form.cleaned_data['set_rest'],
                                    exercise_rest = form.cleaned_data['exercise_rest'],
                                    default_reps = form.cleaned_data['exercise_reps'],
                                    default_time = form.cleaned_data['exercise_time'],
                                    default_mode = form.cleaned_data['exercise_mode'],
                                    circuits = [])

        # create a list of circuit info for each circuit
        for circuitIndex in range (0, workout_info.num_circuits):
            circuit_info = CircuitInfo(name = "Circuit " + str(circuitIndex + 1), exercises = [])
            workout_info.circuits.append(circuit_info)

            # for each exercise in the exercise list create exercise info
            exercise_list = (form.cleaned_data["exercises_" + str(circuitIndex + 1)]).split(',')
            for exerciseIndex in range (0, len(exercise_list)):
                exercise_info = ExerciseInfo(exercise_id = int(exercise_list[exerciseIndex]),
                                                exercise_name = exercise_list[exerciseIndex],
                                                exercise_mode = form.cleaned_data['exercise_mode_' + str(circuitIndex + 1) + "_" + str(exerciseIndex + 1)],
                                                exercise_quantity = form.cleaned_data['exercise_quantity_' + str(circuitIndex + 1) + "_" + str(exerciseIndex + 1)]
                                                )
                circuit_info.exercises.append(exercise_info)

        return workout_info

    def form_check_fields(self, form):
        set_rest = form.cleaned_data['set_rest']
        exercise_rest = form.cleaned_data['exercise_rest']
        session_client = form.cleaned_data['session_client']
        session_date = form.cleaned_data['session_date']
        session_time = form.cleaned_data['session_time']
        exercise_reps = form.cleaned_data['exercise_reps']
        exercise_time = form.cleaned_data['exercise_time']
        circuit_sets = form.cleaned_data['circuit_sets']
        number_of_circuits = form.cleaned_data['number_of_circuits']
        exercise_mode = form.cleaned_data['exercise_mode']

        exercises_1 = form.cleaned_data['exercises_1']
        exercises_2 = form.cleaned_data['exercises_2']
        exercises_3 = form.cleaned_data['exercises_3']
        exercises_4 = form.cleaned_data['exercises_4']
        exercises_5 = form.cleaned_data['exercises_5']

        exercise_mode_1_1 = form.cleaned_data['exercise_mode_1_1']
        exercise_mode_1_2 = form.cleaned_data['exercise_mode_1_2']
        exercise_mode_1_3 = form.cleaned_data['exercise_mode_1_3']
        exercise_mode_1_4 = form.cleaned_data['exercise_mode_1_4']
        exercise_mode_1_5 = form.cleaned_data['exercise_mode_1_5']
        exercise_mode_1_6 = form.cleaned_data['exercise_mode_1_6']
        exercise_mode_1_7 = form.cleaned_data['exercise_mode_1_7']
        exercise_mode_1_8 = form.cleaned_data['exercise_mode_1_8']
        exercise_mode_1_9 = form.cleaned_data['exercise_mode_1_9']
        exercise_mode_1_10 = form.cleaned_data['exercise_mode_1_10']
        exercise_mode_1_11 = form.cleaned_data['exercise_mode_1_11']
        exercise_mode_1_12 = form.cleaned_data['exercise_mode_1_12']
        exercise_mode_1_13 = form.cleaned_data['exercise_mode_1_13']
        exercise_mode_1_14 = form.cleaned_data['exercise_mode_1_14']
        exercise_mode_1_15 = form.cleaned_data['exercise_mode_1_15']
        exercise_mode_2_1 = form.cleaned_data['exercise_mode_2_1']
        exercise_mode_2_2 = form.cleaned_data['exercise_mode_2_2']
        exercise_mode_2_3 = form.cleaned_data['exercise_mode_2_3']
        exercise_mode_2_4 = form.cleaned_data['exercise_mode_2_4']
        exercise_mode_2_5 = form.cleaned_data['exercise_mode_2_5']
        exercise_mode_2_6 = form.cleaned_data['exercise_mode_2_6']
        exercise_mode_2_7 = form.cleaned_data['exercise_mode_2_7']
        exercise_mode_2_8 = form.cleaned_data['exercise_mode_2_8']
        exercise_mode_2_9 = form.cleaned_data['exercise_mode_2_9']
        exercise_mode_2_10 = form.cleaned_data['exercise_mode_2_10']
        exercise_mode_2_11 = form.cleaned_data['exercise_mode_2_11']
        exercise_mode_2_12 = form.cleaned_data['exercise_mode_2_12']
        exercise_mode_2_13 = form.cleaned_data['exercise_mode_2_13']
        exercise_mode_2_14 = form.cleaned_data['exercise_mode_2_14']
        exercise_mode_2_15 = form.cleaned_data['exercise_mode_2_15']
        exercise_mode_3_1 = form.cleaned_data['exercise_mode_3_1']
        exercise_mode_3_2 = form.cleaned_data['exercise_mode_3_2']
        exercise_mode_3_3 = form.cleaned_data['exercise_mode_3_3']
        exercise_mode_3_4 = form.cleaned_data['exercise_mode_3_4']
        exercise_mode_3_5 = form.cleaned_data['exercise_mode_3_5']
        exercise_mode_3_6 = form.cleaned_data['exercise_mode_3_6']
        exercise_mode_3_7 = form.cleaned_data['exercise_mode_3_7']
        exercise_mode_3_8 = form.cleaned_data['exercise_mode_3_8']
        exercise_mode_3_9 = form.cleaned_data['exercise_mode_3_9']
        exercise_mode_3_10 = form.cleaned_data['exercise_mode_3_10']
        exercise_mode_3_11 = form.cleaned_data['exercise_mode_3_11']
        exercise_mode_3_12 = form.cleaned_data['exercise_mode_3_12']
        exercise_mode_3_13 = form.cleaned_data['exercise_mode_3_13']
        exercise_mode_3_14 = form.cleaned_data['exercise_mode_3_14']
        exercise_mode_3_15 = form.cleaned_data['exercise_mode_3_15']
        exercise_mode_4_1 = form.cleaned_data['exercise_mode_4_1']
        exercise_mode_4_2 = form.cleaned_data['exercise_mode_4_2']
        exercise_mode_4_3 = form.cleaned_data['exercise_mode_4_3']
        exercise_mode_4_4 = form.cleaned_data['exercise_mode_4_4']
        exercise_mode_4_5 = form.cleaned_data['exercise_mode_4_5']
        exercise_mode_4_6 = form.cleaned_data['exercise_mode_4_6']
        exercise_mode_4_7 = form.cleaned_data['exercise_mode_4_7']
        exercise_mode_4_8 = form.cleaned_data['exercise_mode_4_8']
        exercise_mode_4_9 = form.cleaned_data['exercise_mode_4_9']
        exercise_mode_4_10 = form.cleaned_data['exercise_mode_4_10']
        exercise_mode_4_11 = form.cleaned_data['exercise_mode_4_11']
        exercise_mode_4_12 = form.cleaned_data['exercise_mode_4_12']
        exercise_mode_4_13 = form.cleaned_data['exercise_mode_4_13']
        exercise_mode_4_14 = form.cleaned_data['exercise_mode_4_14']
        exercise_mode_4_15 = form.cleaned_data['exercise_mode_4_15']
        exercise_mode_5_1 = form.cleaned_data['exercise_mode_5_1']
        exercise_mode_5_2 = form.cleaned_data['exercise_mode_5_2']
        exercise_mode_5_3 = form.cleaned_data['exercise_mode_5_3']
        exercise_mode_5_4 = form.cleaned_data['exercise_mode_5_4']
        exercise_mode_5_5 = form.cleaned_data['exercise_mode_5_5']
        exercise_mode_5_6 = form.cleaned_data['exercise_mode_5_6']
        exercise_mode_5_7 = form.cleaned_data['exercise_mode_5_7']
        exercise_mode_5_8 = form.cleaned_data['exercise_mode_5_8']
        exercise_mode_5_9 = form.cleaned_data['exercise_mode_5_9']
        exercise_mode_5_10 = form.cleaned_data['exercise_mode_5_10']
        exercise_mode_5_11 = form.cleaned_data['exercise_mode_5_11']
        exercise_mode_5_12 = form.cleaned_data['exercise_mode_5_12']
        exercise_mode_5_13 = form.cleaned_data['exercise_mode_5_13']
        exercise_mode_5_14 = form.cleaned_data['exercise_mode_5_14']
        exercise_mode_5_15 = form.cleaned_data['exercise_mode_5_15']

        exercise_quantity_1_1 = form.cleaned_data['exercise_quantity_1_1']
        exercise_quantity_1_2 = form.cleaned_data['exercise_quantity_1_2']
        exercise_quantity_1_3 = form.cleaned_data['exercise_quantity_1_3']
        exercise_quantity_1_4 = form.cleaned_data['exercise_quantity_1_4']
        exercise_quantity_1_5 = form.cleaned_data['exercise_quantity_1_5']
        exercise_quantity_1_6 = form.cleaned_data['exercise_quantity_1_6']
        exercise_quantity_1_7 = form.cleaned_data['exercise_quantity_1_7']
        exercise_quantity_1_8 = form.cleaned_data['exercise_quantity_1_8']
        exercise_quantity_1_9 = form.cleaned_data['exercise_quantity_1_9']
        exercise_quantity_1_10 = form.cleaned_data['exercise_quantity_1_10']
        exercise_quantity_1_11 = form.cleaned_data['exercise_quantity_1_11']
        exercise_quantity_1_12 = form.cleaned_data['exercise_quantity_1_12']
        exercise_quantity_1_13 = form.cleaned_data['exercise_quantity_1_13']
        exercise_quantity_1_14 = form.cleaned_data['exercise_quantity_1_14']
        exercise_quantity_1_15 = form.cleaned_data['exercise_quantity_1_15']
        exercise_quantity_2_1 = form.cleaned_data['exercise_quantity_2_1']
        exercise_quantity_2_2 = form.cleaned_data['exercise_quantity_2_2']
        exercise_quantity_2_3 = form.cleaned_data['exercise_quantity_2_3']
        exercise_quantity_2_4 = form.cleaned_data['exercise_quantity_2_4']
        exercise_quantity_2_5 = form.cleaned_data['exercise_quantity_2_5']
        exercise_quantity_2_6 = form.cleaned_data['exercise_quantity_2_6']
        exercise_quantity_2_7 = form.cleaned_data['exercise_quantity_2_7']
        exercise_quantity_2_8 = form.cleaned_data['exercise_quantity_2_8']
        exercise_quantity_2_9 = form.cleaned_data['exercise_quantity_2_9']
        exercise_quantity_2_10 = form.cleaned_data['exercise_quantity_2_10']
        exercise_quantity_2_11 = form.cleaned_data['exercise_quantity_2_11']
        exercise_quantity_2_12 = form.cleaned_data['exercise_quantity_2_12']
        exercise_quantity_2_13 = form.cleaned_data['exercise_quantity_2_13']
        exercise_quantity_2_14 = form.cleaned_data['exercise_quantity_2_14']
        exercise_quantity_2_15 = form.cleaned_data['exercise_quantity_2_15']
        exercise_quantity_3_1 = form.cleaned_data['exercise_quantity_3_1']
        exercise_quantity_3_2 = form.cleaned_data['exercise_quantity_3_2']
        exercise_quantity_3_3 = form.cleaned_data['exercise_quantity_3_3']
        exercise_quantity_3_4 = form.cleaned_data['exercise_quantity_3_4']
        exercise_quantity_3_5 = form.cleaned_data['exercise_quantity_3_5']
        exercise_quantity_3_6 = form.cleaned_data['exercise_quantity_3_6']
        exercise_quantity_3_7 = form.cleaned_data['exercise_quantity_3_7']
        exercise_quantity_3_8 = form.cleaned_data['exercise_quantity_3_8']
        exercise_quantity_3_9 = form.cleaned_data['exercise_quantity_3_9']
        exercise_quantity_3_10 = form.cleaned_data['exercise_quantity_3_10']
        exercise_quantity_3_11 = form.cleaned_data['exercise_quantity_3_11']
        exercise_quantity_3_12 = form.cleaned_data['exercise_quantity_3_12']
        exercise_quantity_3_13 = form.cleaned_data['exercise_quantity_3_13']
        exercise_quantity_3_14 = form.cleaned_data['exercise_quantity_3_14']
        exercise_quantity_3_15 = form.cleaned_data['exercise_quantity_3_15']
        exercise_quantity_4_1 = form.cleaned_data['exercise_quantity_4_1']
        exercise_quantity_4_2 = form.cleaned_data['exercise_quantity_4_2']
        exercise_quantity_4_3 = form.cleaned_data['exercise_quantity_4_3']
        exercise_quantity_4_4 = form.cleaned_data['exercise_quantity_4_4']
        exercise_quantity_4_5 = form.cleaned_data['exercise_quantity_4_5']
        exercise_quantity_4_6 = form.cleaned_data['exercise_quantity_4_6']
        exercise_quantity_4_7 = form.cleaned_data['exercise_quantity_4_7']
        exercise_quantity_4_8 = form.cleaned_data['exercise_quantity_4_8']
        exercise_quantity_4_9 = form.cleaned_data['exercise_quantity_4_9']
        exercise_quantity_4_10 = form.cleaned_data['exercise_quantity_4_10']
        exercise_quantity_4_11 = form.cleaned_data['exercise_quantity_4_11']
        exercise_quantity_4_12 = form.cleaned_data['exercise_quantity_4_12']
        exercise_quantity_4_13 = form.cleaned_data['exercise_quantity_4_13']
        exercise_quantity_4_14 = form.cleaned_data['exercise_quantity_4_14']
        exercise_quantity_4_15 = form.cleaned_data['exercise_quantity_4_15']
        exercise_quantity_5_1 = form.cleaned_data['exercise_quantity_5_1']
        exercise_quantity_5_2 = form.cleaned_data['exercise_quantity_5_2']
        exercise_quantity_5_3 = form.cleaned_data['exercise_quantity_5_3']
        exercise_quantity_5_4 = form.cleaned_data['exercise_quantity_5_4']
        exercise_quantity_5_5 = form.cleaned_data['exercise_quantity_5_5']
        exercise_quantity_5_6 = form.cleaned_data['exercise_quantity_5_6']
        exercise_quantity_5_7 = form.cleaned_data['exercise_quantity_5_7']
        exercise_quantity_5_8 = form.cleaned_data['exercise_quantity_5_8']
        exercise_quantity_5_9 = form.cleaned_data['exercise_quantity_5_9']
        exercise_quantity_5_10 = form.cleaned_data['exercise_quantity_5_10']
        exercise_quantity_5_11 = form.cleaned_data['exercise_quantity_5_11']
        exercise_quantity_5_12 = form.cleaned_data['exercise_quantity_5_12']
        exercise_quantity_5_13 = form.cleaned_data['exercise_quantity_5_13']
        exercise_quantity_5_14 = form.cleaned_data['exercise_quantity_5_14']
        exercise_quantity_5_15 = form.cleaned_data['exercise_quantity_5_15']