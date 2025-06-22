from dataclasses import dataclass
from datetime import date, time
from fitnessApp.choices import MODE_CHOICES
from typing import List

@dataclass
class SessionInfo:
    client_id: int
    scheduled_date: date
    scheduled_time: time

@dataclass
class ExerciseInfo:
    exercise_id: int
    exercise_name: str
    exercise_mode: str
    exercise_quantity: int

@dataclass
class CircuitInfo:
    name: str
    exercises: List[ExerciseInfo]

@dataclass
class WorkoutInfo:
    name: str
    num_circuits: int
    num_sets: int
    set_rest: int
    exercise_rest: int
    default_reps: int
    default_time: int
    default_mode: str
    circuits: List[CircuitInfo]



