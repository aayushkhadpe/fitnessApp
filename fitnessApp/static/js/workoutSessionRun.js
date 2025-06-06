let remaining = totalSeconds;

const radius = 45;
const circumference = 2 * Math.PI * radius;
const progressCircle = document.querySelector('.circle-progress');
progressCircle.style.strokeDasharray = circumference;
progressCircle.style.strokeDashoffset = 0;
const audioContext = new (window.AudioContext || window.webkitAudioContext)();

let isPaused = false;
let interval;

setProgress(1.0 - (1.0 / totalSeconds));
startTimer();

const pauseButton = document.getElementById("pause-button");

pauseButton.addEventListener("click", () =>
{
  isPaused = !isPaused;
  if (isPaused) 
  {
    document.getElementById("pause-resume-button").classList.remove("bi-pause-circle")
    document.getElementById("pause-resume-button").classList.add("bi-play-circle")
    // hideElement("pause-image")
    // showElement("play-image")
  }
  else 
  {
    document.getElementById("pause-resume-button").classList.add("bi-pause-circle")
    document.getElementById("pause-resume-button").classList.remove("bi-play-circle")
    // hideElement("play-image")
    // showElement("pause-image")
  }
}
);

updateProgress();


function disableElement(id)
{
  document.getElementById(id).disabled = true;
}

function enableElement(id)
{
  document.getElementById(id).disabled = false;
}

function hideElement(id)
{
  document.getElementById(id).style.visibility = "hidden";
}

function showElement(id)
{
  document.getElementById(id).style.visibility = "visible";
}

function formatTime(seconds)
{
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function setProgress(percent)
{
  const offset = circumference * (1 - percent);
  if (progressCircle.style.transitionDuration == '1ms' && totalSeconds - remaining == 1)
  {
    progressCircle.style.transitionDuration = '1s';
  }
  progressCircle.style.strokeDashoffset = offset;

  if (remaining <= 6)
  {
    playBeep( remaining == 1 ? 800 : 200);
  }

}

function playBeep(duration)
{
    const oscillator = audioContext.createOscillator();
    oscillator.type = 'triangle';
    oscillator.frequency.value = 500;
    oscillator.connect(audioContext.destination);
    oscillator.start();

    setTimeout(() => { oscillator.stop(); }, duration);
}

function startTimer()
{ 

  // when timer starts, gray out video and hide the exercise and reps div, show pause button
  showElement('grey');
  showElement('next-up-pill')
  //hideElement('exercise-div');
  //hideElement('reps-div');
  enableElement("pause-button");
  hideElement('exercise-message');
  showElement('rest-message')

  const timeText = document.getElementById("time-text");
  timeText.textContent = formatTime(remaining);

  interval = setInterval(() =>
  {
    if (isPaused)
      return;

    remaining--;
    const progress = ((remaining - 1) / totalSeconds);
    
    if (remaining > 0)
      setProgress(progress);

    timeText.textContent = formatTime(remaining);

    if (remaining <= 0)
    {
      // a timer just got done. it could be rest timer or the timed exercise timer.
      clearInterval(interval);
      timeText.textContent = "00:00";

      //playBeep(400);

      switch (check)
      {
        // timer for rest part of timed exercise was done.
        case "TIME":
          check = "RUNNING";
          totalSeconds = exerciseTime;
          remaining = totalSeconds;
          progressCircle.style.transitionDuration = '1ms';
          progressCircle.style.stroke = 'green';
          setProgress(1);
          startTimer();
          hideElement('rest-message');
          showElement('exercise-message');

          // rest timer was done. hide the rest timer related divs (gray overlay on video, and rest message line) and display the exercise div
          //hideElement('rest-div');
          //showElement('exercise-div');
          hideElement('grey');
          hideElement('next-up-pill')

          break;

        // timer for run part of timed exercise was done. submit form to go to next exercise
        case "RUNNING":
          document.getElementById('next-form').submit();
          break;

        // rest timer was done for reps based exercise. switch the divs.
        case "REPS":
          //hideElement('rest-div');
          hideElement('timer');
          hideElement('restart-timer-div');
          hideElement('skip-rest-timer-div');
          hideElement('timer-div');
          hideElement('rest-message');
          showElement('exercise-message');

          //showElement('exercise-div');
          //showElement('reps-div');

          hideElement('grey');
          hideElement('next-up-pill')
          disableElement("pause-button");

          break;
      }
    }
  }, 1000);
}

function updateProgress() {
      const progress = (current_initial / current_final) * 100;

      const progressBar = document.getElementById('progressBar');
      progressBar.style.background = 'green';
      progressBar.style.width = progress + '%';
    }

function restartTimer() {
  remaining = totalSeconds;
  progressCircle.style.transitionDuration = '1ms';
  const timeText = document.getElementById("time-text");
  timeText.textContent = formatTime(remaining);
  setProgress(1);
}

function skipTimer() {
  remaining = 0;
  setProgress(0);
}






