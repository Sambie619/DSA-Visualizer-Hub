async function visualize() {
  const urlParams = new URLSearchParams(window.location.search);
  const algo = urlParams.get("algo");
  const data = urlParams.get("data");

  const response = await fetch(`/get_steps?algo=${algo}&data=${data}`);
  const stepsData = await response.json();
  const steps = stepsData.steps; // actual array of steps
  const container = document.getElementById("visualizer");
  container.innerHTML = "";

  if (steps.length === 0) {
    container.innerHTML = "<p>No steps to show.</p>";
    return;
  }

  // --- Create initial bars ---
  let arr = steps[0].array;
  arr.forEach((value) => {
    const bar = document.createElement("div");
    bar.className = "bar";
    bar.style.height = `${value * 20}px`;
    bar.style.width = "25px";
    bar.style.margin = "2px";
    bar.style.backgroundColor = "#4CAF50";
    container.appendChild(bar);
  });

  const bars = container.getElementsByClassName("bar");

  // --- Animate steps ---
  for (let step of steps) {
    await new Promise((r) => setTimeout(r, 400)); // delay for animation

    // Reset all bars to green by default
    for (let b of bars) {
      b.style.backgroundColor = "#4CAF50";
    }

    if (step.type === "compare") {
      bars[step.i].style.backgroundColor = "red";
      bars[step.j].style.backgroundColor = "red";
    } else if (step.type === "swap") {
      bars[step.i].style.height = `${step.array[step.i] * 20}px`;
      bars[step.j].style.height = `${step.array[step.j] * 20}px`;
      bars[step.i].style.backgroundColor = "orange";
      bars[step.j].style.backgroundColor = "orange";
    } else if (step.type === "key_pick" || step.type === "select_min") {
      bars[step.i].style.backgroundColor = "blue";
    } else if (step.type === "overwrite" || step.type === "insert") {
      bars[step.i].style.height = `${step.array[step.i] * 20}px`;
      bars[step.i].style.backgroundColor = "purple";
    }

    // Update all heights for current snapshot
    for (let i = 0; i < bars.length; i++) {
      bars[i].style.height = `${step.array[i] * 20}px`;
    }
  }
}

// Start button event
document.getElementById("startBtn").addEventListener("click", visualize);
