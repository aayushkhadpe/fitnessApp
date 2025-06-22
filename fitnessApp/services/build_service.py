from fitnessApp.data import *
from fitnessApp.models import *

def create_workout(workout_info: WorkoutInfo) -> Workout:

    # create workout
    workout = Workout.objects.create(name=workout_info.name)
    workout.save()

    # create workout circuit for each circuit info
    for circuit_info in workout_info.circuits:
        workout_circuit = WorkoutCircuit.objects.create(workout=workout,
                                                        name=circuit_info.name,
                                                        sets=workout_info.num_sets,
                                                        set_rest=workout_info.set_rest,
                                                        exercise_rest=workout_info.exercise_rest
                                                        )
        workout_circuit.save()

        # create circuit exercise for each exercise info in circuit info
        for exercise_info in circuit_info.exercises:
            circuit_exercise = CircuitExercise.objects.create(circuit=workout_circuit,
                                                              exercise_id=exercise_info.exercise_id,
                                                              mode=exercise_info.exercise_mode
                                                              )
            # set the reps or time based on mode
            if exercise_info.exercise_mode == "REPS":
                circuit_exercise.reps = exercise_info.exercise_quantity  
            else:
                circuit_exercise.time = exercise_info.exercise_quantity

            circuit_exercise.save()

    return workout

def create_workout_session(session_info: SessionInfo, workout_info: WorkoutInfo) -> WorkoutSession:

    # create the workout
    workout = create_workout(workout_info)

    # create the workout session
    workout_session = WorkoutSession.objects.create(workout=workout, 
                                                    person_id=session_info.client_id, 
                                                    scheduled_date=session_info.scheduled_date, 
                                                    scheduled_time=session_info.scheduled_time, 
                                                    )
    workout_session.save()

    # create workout session steps
    create_workout_session_steps(workout_session)

    return workout_session

def create_workout_session_steps(workout_session: WorkoutSession) -> WorkoutSession:
    seq = 1
    before = 10

    for circuit in workout_session.workout.workoutcircuit_set.all():
        for setnumber in range(1, circuit.sets + 1):

            circuitexercises = circuit.circuitexercise_set.all()
            lastelement = circuitexercises.last()
            firstelement = circuitexercises.first()
            
            for circuitexercise in circuitexercises:

                after = circuit.set_rest if circuitexercise == lastelement else circuit.exercise_rest

                WorkoutSessionStep.objects.create(
                    workoutSession = workout_session,
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
    
    return workout_session