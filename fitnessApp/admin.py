from django.contrib import admin
from fitnessApp.models import *

# Register your models here.

@admin.register(FitnessAppUser)
class FitnessAppUserAdmin(admin.ModelAdmin):
    pass
    list_display = ('email', 'is_active', 'is_staff', 'date_joined', 'last_login', 'person__first_name', 'person__last_name', 'person__email', 'person__phone_number',)
    search_fields = ('email', 'person__first_name', 'person__last_name', 'person__email', 'person__phone_number',)

@admin.register(FitnessAppPerson)
class FitnessAppPersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number',)
    search_fields = ('first_name', 'last_name', 'email', 'phone_number',)

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'difficulty_level', 'target', 'public_flag', 'personalized_flag', 'video_id', 'creator', )
    search_fields = ('name', 'duration', 'difficulty_level', 'target', 'public_flag', 'personalized_flag', 'creator',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'public_flag', 'weight_flag', 'video_id', 'creator', )
    search_fields = ('name', 'public_flag', 'weight_flag', 'creator',)