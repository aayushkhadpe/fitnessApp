from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DetailView, FormView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from fitnessApp.data import *
from fitnessApp.models import *
from fitnessApp.forms import *
from fitnessApp.services import *

class WorkoutSessionCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutSession
    template_name = "workoutsession_create.html"
    form_class = WorkoutSessionCreateForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        workout_id = self.kwargs['workout_id']
        context['workout'] = Workout.objects.get(pk=workout_id)

        return context;

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):

        form.instance.workout_id = self.kwargs['workout_id']
        form.instance.person_id = form.cleaned_data['person_id']

        response = super().form_valid(form)

        self.object.creator_id = self.request.user.person.id
        self.object.save()
        
        create_workout_session_steps(self.object)

        return response

class WorkoutSessionDoView(LoginRequiredMixin, DetailView):
    model = WorkoutSession
    template_name = "do_session/do_session_main.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        steps = context['object'].workoutsessionstep_set.all().values('id', 'set', 'circuit__name', 'exercise__name', 'workoutSession__id', 'sequence_number', 'rest_before', 'circuit_exercise__mode', 'circuit_exercise__time', 'circuit_exercise__reps', 'exercise_number')
        context['steps'] = list(steps)

        return context

class BaseBuildView(LoginRequiredMixin, FormView):
    template_name = 'builder/builder_main.html'
    success_url = reverse_lazy("home")
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exercises = Exercise.objects.filter(Q(creator=self.request.user.person) | Q(public_flag="True")).values('id', 'name')
        context['num_circuit_exercises'] = range(15)
        context['exercises'] = list(exercises)

        return context

    def create_workout_info(self, form, creator_id):
        
        # create workout info
        workout_info = WorkoutInfo( name = "",
                                    personalized_flag=False,
                                    duration = 60,
                                    target = "UNSPECIFIED",
                                    difficulty_level = "UNSPECIFIED",
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
            for exerciseIndex, exerciseValue in enumerate(exercise_list):
                
                # if the exerciseValue is digit, it is id, otherwise it is a name of new exercise
                exercise_id = None
                if exerciseValue.isdigit():
                    exercise_id = int(exerciseValue)
                else:
                    new_exercise = Exercise.objects.create(name = exerciseValue, creator_id=creator_id)
                    new_exercise.save()
                    exercise_id = new_exercise.id

                exercise_info = ExerciseInfo(exercise_id = exercise_id,
                                            exercise_mode = form.cleaned_data['exercise_mode_' + str(circuitIndex + 1) + "_" + str(exerciseIndex + 1)],
                                            exercise_quantity = form.cleaned_data['exercise_quantity_' + str(circuitIndex + 1) + "_" + str(exerciseIndex + 1)],
                                            exercise_rest = form.cleaned_data['exercise_rest_' + str(circuitIndex + 1) + "_" + str(exerciseIndex + 1)],
                                            )
                    
                circuit_info.exercises.append(exercise_info)
                    
        return workout_info

class WorkoutSessionBuildView(BaseBuildView):
    form_class = WorkoutSessionBuildForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buildMode'] = "SESSION"

        return context
    
    def form_valid(self, form):
        # Process the valid form data here

        session_info = SessionInfo(client_id = 0, 
                                    scheduled_date = form.cleaned_data['session_date'],
                                    scheduled_time = form.cleaned_data['session_time'])
        
        workout_info = self.create_workout_info(form, self.request.user.person.id)

        if (self.request.user.person.coach_flag == True):
            session_info.client_id = int(form.cleaned_data['session_client'])
        else:
            session_info.client_id = self.request.user.person.id

        workout_info.personalized_flag = True
        workout_info.name = "Personalized Session"
        
        create_workout_session(session_info, workout_info, self.request.user.person.id)

        # Redirect to the success URL
        return super().form_valid(form)
    
class WorkoutBuildView(BaseBuildView):
    form_class = WorkoutBuildForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['buildMode'] = "WORKOUT"

        return context
    
    def form_valid(self, form):
        # Process the valid form data here
        
        workout_info = self.create_workout_info(form, self.request.user.person.id)
        # workout_info.name = "Workout @ " + str(session_info.scheduled_date)
        workout_info.name = form.cleaned_data['workout_name']
        workout_info.duration = form.cleaned_data['workout_duration']
        workout_info.difficulty_level = form.cleaned_data['workout_difficulty_level']
        workout_info.target = form.cleaned_data['workout_target']

        create_workout(workout_info, self.request.user.person.id)

        # Redirect to the success URL
        return super().form_valid(form)
    
class WorkoutSessionRescheduleView(LoginRequiredMixin, UpdateView):
    model = WorkoutSession
    form_class = WorkoutSessionRescheduleForm
    success_url = reverse_lazy("home")
    template_name = "workoutsession_reschedule.html"

class WorkoutSessionDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutSession
    success_url = reverse_lazy("home")
    template_name = "workoutsession_delete.html"
    
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
