/************ Classes ************/

class DoTimer {
    #isTimer = true;
    #isRest = true;
    #time = 0;
    #textElementId = null;
    #circleSvgId = null;
    #doneCallback = null;
    #easyTimer = null;

    startTimer(isTimer, time, textElementId, circleSvgId, doneCallback, isRest) {
        this.stopTimer();

        this.#isTimer = isTimer;
        this.#isRest = isRest;
        this.#time = time;
        this.#textElementId = textElementId;
        this.#circleSvgId = circleSvgId;
        this.#doneCallback = doneCallback;

        this.#createTimer();
    }

    #createTimer() {
        this.#easyTimer = new Timer();
        this.#easyTimer.start({ countdown: this.#isTimer, startValues: { seconds: this.#time } });

        document.getElementById(this.#textElementId).textContent = formatTime(this.#easyTimer.getTotalTimeValues().seconds);

        var textElementId = this.#textElementId;
        var easyTimer = this.#easyTimer;
        var doneCallback = this.#doneCallback;
        var isTimer = this.#isTimer;
        var isRest = this.#isRest;
        var index = currentStep - 1;
        var text = "Begin " + steps[index].exercise__name + " for " + (steps[index].circuit_exercise__mode == "REPS" ? steps[index].circuit_exercise__reps + " reps" : steps[index].circuit_exercise__time + " seconds")

        this.#easyTimer.addEventListener('secondsUpdated', function (e) {
            document.getElementById(textElementId).textContent = formatTime(easyTimer.getTotalTimeValues().seconds);

            if (isTimer && easyTimer.getTotalTimeValues().seconds == 11 && isRest) {
                speak(text);
            }

            if (isTimer && easyTimer.getTotalTimeValues().seconds <= 6 && easyTimer.getTotalTimeValues().seconds != 0) {
                playBeep(easyTimer.getTotalTimeValues().seconds == 1 ? 800 : 200);
            }
        });

        this.#easyTimer.addEventListener('targetAchieved', function (e) {
            doneCallback();
        });
    }

    skipTimer() {
        if (this.#easyTimer == null)
            return;

        this.stopTimer();
        this.#doneCallback();
    }

    restartTimer() {
        if (this.#easyTimer != null)
            this.stopTimer();
        this.#createTimer();
    }

    playPauseTimer() {
        if (this.#easyTimer == null)
            return;

        if (this.#easyTimer.isPaused())
            this.#easyTimer.start();
        else
            this.#easyTimer.pause();
    }

    isPaused() {
        return this.#easyTimer.isPaused();
    }

    stopTimer() {
        if (this.#easyTimer != null) {
            this.#easyTimer.stop();
            this.#easyTimer = null;
        }
    }
}

/************ Global variables ************/

var audioContext = null;
var doTimer = new DoTimer();

var wakeLock = null;

var steps = JSON.parse(document.getElementById('id-steps-json').textContent);
var numSteps = steps.length;

var workoutSessionId = JSON.parse(document.getElementById('id-workout-session-id').textContent);
var currentStep = JSON.parse(document.getElementById('id-current-step-sequence').textContent);

var csrfToken = getCookie('csrftoken');

if (currentStep == '') {
    currentStep = 1;
}

document.getElementById("id-start-workout-button").addEventListener("click", startWorkout);
document.getElementById("id-previous-button").addEventListener("click", previousStep);
document.getElementById("id-pause-button").addEventListener("click", playPauseTimer);
document.getElementById("id-next-button").addEventListener("click", nextStep);

var allTimers = document.querySelectorAll(".dosession-timer-restart");

for (item of allTimers) {
    item.addEventListener("click", restartTimer);
}

var allTimers = document.querySelectorAll(".dosession-timer-skip");

for (item of allTimers) {
    item.addEventListener("click", skipTimer);
}

if (currentStep == steps.length) {
    set_display_none("id-do-session-start");
    set_display_none("id-do-session-step");
    set_display_block("id-do-session-finish");
}

/************ Functions ************/

function playBeep(duration) {
    const oscillator = audioContext.createOscillator();
    oscillator.type = 'triangle';
    oscillator.frequency.value = 500;
    oscillator.connect(audioContext.destination);
    oscillator.start();

    setTimeout(() => { oscillator.stop(); }, duration);
}

function setupWakeLock() {
    if ("wakeLock" in navigator) {
        isSupported = true;
        console.log("Screen Wake Lock API supported!");
    }
    else {
        wakeButton.disabled = true;
        console.log("Wake lock is not supported by this browser.");
    }

    // create an async function to request a wake lock on visibility change

    document.addEventListener("visibilitychange", async () => {
        if (wakeLock !== null && document.visibilityState === "visible") {
            wakeLock = await navigator.wakeLock.request("screen");
            console.log("Wake Lock is active after visibility change!");
        }
    });
}

async function requestWakeLock() {
    try {
        wakeLock = await navigator.wakeLock.request("screen");
        console.log("Wake Lock is active!");
    }
    catch (err) {
        // The Wake Lock request has failed - usually system related, such as battery.
        console.log(`${err.name}, ${err.message}`);
    }

    wakeLock.addEventListener("release", () => {
        // the wake lock has been released
        console.log("Wake Lock has been released");
    });
}

function startWorkout() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    audioContext.resume();

    set_display_none("id-do-session-start");
    set_display_block("id-do-session-step");

    updateStep();

    setupWakeLock();

    requestWakeLock();

    updateWorkoutSession(workoutSessionId, { status: "INPROGRESS" });
}

function updateStep() {
    var index = currentStep - 1;

    if (currentStep == 1) {
        disableElement("id-previous-button");
    }
    else {
        enableElement("id-previous-button");
    }

    document.getElementById("id-progress-bar-circuit").innerText = steps[index].circuit__name;
    document.getElementById("id-progress-bar-set").innerText = steps[index].set;
    document.getElementById("id-progress-bar-exercise").innerText = steps[index].exercise_number;

    document.getElementById("id-fraction-numerator").innerText = currentStep;
    document.getElementById("id-fraction-denominator").innerText = steps.length;

    document.getElementById("id-exercise-name-field").innerText = steps[index].exercise__name;
    document.getElementById("id-rest-time-field").innerText = steps[index].rest_before;

    if (steps[index].circuit_exercise__mode == "REPS") {
        document.getElementById("id-mode-type-display").innerText = "REPS";
        document.getElementById("id-mode-quantity-display").innerText = steps[index].circuit_exercise__reps;
        document.getElementById("id-mode-quantity-units").innerText = " reps"
    }
    else {
        document.getElementById("id-mode-type-display").innerText = "TIME";
        document.getElementById("id-mode-quantity-display").innerText = steps[index].circuit_exercise__time;
        document.getElementById("id-mode-quantity-units").innerText = " secs"
    }

    updateProgress();

    startRest();

    document.getElementById("id-pause-resume-button-icon").classList.add("bi-pause-circle");
    document.getElementById("id-pause-resume-button-icon").classList.remove("bi-play-circle");

    speak("Rest for " + steps[index].rest_before + " seconds, then " + steps[index].exercise__name + " for " + (steps[index].circuit_exercise__mode == "REPS" ? steps[index].circuit_exercise__reps + " reps" : steps[index].circuit_exercise__time + " seconds"));

}

function speak(text)
{
    const synth = window.speechSynthesis;
    synth.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    synth.speak(utterance);    
}

function startRest() {
    set_display_none("id-div-timer-time");
    set_display_none("id-div-timer-reps");
    set_display_null("id-div-timer-rest");

    document.getElementById("id-rest-div").classList.remove("opacity-50");
    document.getElementById("id-work-div").classList.add("opacity-50");
    document.getElementById("id-exercise-div").classList.add("opacity-50");
    set_display_null("id-nextup-div");

    doTimer.startTimer(true, steps[currentStep - 1].rest_before, "id-time-text-rest", "circle-progress-rest", startWork, true);
}

function startWork() {
    set_display_none("id-div-timer-rest");

    if (steps[currentStep - 1].circuit_exercise__mode == "REPS")
        startRepsExercise();
    else
        startTimedExercise();

    document.getElementById("id-rest-div").classList.add("opacity-50");
    document.getElementById("id-work-div").classList.remove("opacity-50");
    document.getElementById("id-exercise-div").classList.remove("opacity-50");
    set_display_none("id-nextup-div");

}

function startRepsExercise() {
    set_display_none("id-div-timer-time");
    set_display_null("id-div-timer-reps");
    doTimer.startTimer(false, 0, "id-time-text-reps", "circle-progress-reps", null, false);
}

function startTimedExercise() {
    set_display_none("id-div-timer-reps");
    set_display_null("id-div-timer-time");
    doTimer.startTimer(true, steps[currentStep - 1].circuit_exercise__time, "id-time-text-time", "circle-progress-time", doneWork, false);
}

function doneWork() {
    nextStep();
}

function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function restartTimer() {
    doTimer.restartTimer();
}

function playPauseTimer() {
    doTimer.playPauseTimer();

    if (doTimer.isPaused()) {
        document.getElementById("id-pause-resume-button-icon").classList.remove("bi-pause-circle");
        document.getElementById("id-pause-resume-button-icon").classList.add("bi-play-circle");
    }
    else {
        document.getElementById("id-pause-resume-button-icon").classList.add("bi-pause-circle");
        document.getElementById("id-pause-resume-button-icon").classList.remove("bi-play-circle");
    }
}

function skipTimer() {
    doTimer.skipTimer();
}

function previousStep() {
    if (currentStep != 1) {
        currentStep--;
        updateWorkoutSession(workoutSessionId, { current_step_sequence: currentStep });
        updateStep();
    }
}

function nextStep() {
    if (currentStep == steps.length) {
        set_display_none("id-do-session-step");
        set_display_block("id-do-session-finish");
        doTimer.stopTimer();
        updateWorkoutSession(workoutSessionId, { status: "COMPLETED" });
    }
    else {
        currentStep++;
        updateWorkoutSession(workoutSessionId, { current_step_sequence: currentStep });
        updateStep();
    }
}

function set_display_block(id) {
    document.getElementById(id).style.display = 'block';
}

// restoring a div to original display state requires it to be set to empty and not none.
function set_display_null(id) {
    document.getElementById(id).style.display = '';
}

function set_display_none(id) {
    document.getElementById(id).style.display = 'none';
}

function disableElement(id) {
    document.getElementById(id).disabled = true;
}

function enableElement(id) {
    document.getElementById(id).disabled = false;
}

function updateProgress() {
    const progress = (currentStep / steps.length) * 100;
    document.getElementById('id-progress-bar').style.width = progress + '%';
}

async function updateWorkoutSession(id, data) {
    try {
        const response = await fetch(`/fitnessApp/api/workoutsessions/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(`HTTP error! status: ${response.status}, details: ${JSON.stringify(errorData)}`);
        }

        const updatedResource = await response.json();
        return updatedResource;
    } catch (error) {
        console.error('Error updating resource:', error);
        throw error;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
