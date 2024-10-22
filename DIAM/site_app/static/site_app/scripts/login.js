const section = document.querySelector(".form-section"),
        overlay = document.querySelector(".overlay"),
        showBtn = document.querySelector(".show-login");

showBtn.addEventListener("click", () => section.classList.add("active"));

overlay.addEventListener("click", () =>
        section.classList.remove("active")
);


let signup = document.querySelector(".signup");
let login = document.querySelector(".login");
let slider = document.querySelector(".slider");
let formulario = document.querySelector(".formulario");

function signup(url) {
    signup.addEventListener("click", () => {
        slider.classList.add("moveslider");
        formulario.classList.add("form-section-move");
    });
}

login.addEventListener("click", () => {
    slider.classList.remove("moveslider");
    formulario.classList.remove("form-section-move");
});
