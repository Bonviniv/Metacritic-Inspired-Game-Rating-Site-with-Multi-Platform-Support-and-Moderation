const sliderEl = document.querySelector(".input-rating")
const sliderValue = document.querySelector(".slider-number1")

sliderEl.addEventListener("input", (event) => {
  const tempSliderValue = event.target.value;
  sliderValue.textContent = tempSliderValue;

  const progress = (tempSliderValue / sliderEl.max) * 100;

  sliderEl.style.background = `linear-gradient(to right, #f50 ${progress}%, #ccc ${progress}%)`;
})