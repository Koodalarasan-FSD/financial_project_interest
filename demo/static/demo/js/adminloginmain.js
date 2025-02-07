/* Showing SignIn and SignUp */

const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});



/* Hiding & Unhiding Password */


let passIcon = document.querySelectorAll(".eye-icon");

passIcon.forEach((icon) => {
  icon.addEventListener("click", () => {
    let passwordInputs = icon.parentElement.querySelectorAll(".password");

    passwordInputs.forEach((input) => {
      //if the input type is password, making it to text
      //and changin icon
      if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("fa-eye", "fa-eye-slash");
        return;
      }

      input.type = "password";
      icon.classList.replace("fa-eye-slash", "fa-eye");
    });
  });
});


