const sliderEl2 = document.querySelector(".input-rating2")
const sliderValue2 = document.querySelector(".slider-number2")

sliderEl2.addEventListener("input", (event) => {
  const tempSliderValue2 = event.target.value;
  sliderValue2.textContent = tempSliderValue2;

  const progress2 = (tempSliderValue2 / sliderEl2.max) * 100;

  sliderEl2.style.background = `linear-gradient(to right, #f50 ${progress2}%, #ccc ${progress2}%)`;
})