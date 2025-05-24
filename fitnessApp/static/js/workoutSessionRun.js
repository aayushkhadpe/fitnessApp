let remaining = totalSeconds;

const radius = 90;
const circumference = 2 * Math.PI * radius;
const progressCircle = document.querySelector('.circle-progress');
progressCircle.style.strokeDasharray = circumference;
progressCircle.style.strokeDashoffset = 0;

let isPaused = false;
let interval;

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
}

function startTimer()
{

  // when timer starts, gray out video and hide the exercise and reps div, show pause button
  showElement('grey');
  hideElement('exercise-div');
  hideElement('reps-div');
  showElement("pause-button");

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

          // rest timer was done. hide the rest timer related divs (gray overlay on video, and rest message line) and display the exercise div
          hideElement('rest-div');
          showElement('exercise-div');
          hideElement('grey');

          break;

        // timer for run part of timed exercise was done. submit form to go to next exercise
        case "RUNNING":
          document.getElementById('next-form').submit();
          break;

        // rest timer was done for reps based exercise. switch the divs.
        case "REPS":
          hideElement('rest-div');
          hideElement('timer-div');

          showElement('exercise-div');
          showElement('reps-div');

          hideElement('grey');
          hideElement("pause-button");
          break;
      }
    }
  }, 1000);

}

setProgress(1.0 - (1.0 / totalSeconds));
startTimer();

const pauseButton = document.getElementById("pause-button");

pauseButton.addEventListener("click", () =>
{
  isPaused = !isPaused;
  pauseButton.textContent = isPaused ? "Resume" : "Pause";
}
);
