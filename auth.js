/**
 * auth.js — handles login.html and register.html forms.
 * On success stores "cc_token" and "cc_user" in localStorage, then
 * redirects to dashboard.html.
 */

const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const alertBox = document.getElementById("loginAlert");
    const btn = document.getElementById("loginBtn");
    const btnText = document.getElementById("loginBtnText");
    const spinner = document.getElementById("loginSpinner");

    alertBox.classList.add("d-none");
    if (!email || !password) {
      alertBox.textContent = "Please enter both email and password.";
      alertBox.classList.remove("d-none");
      return;
    }

    btn.disabled = true;
    btnText.textContent = "Logging in...";
    spinner.classList.remove("d-none");

    try {
      const data = await API.login(email, password);
      localStorage.setItem("cc_token", data.token);
      localStorage.setItem("cc_user", JSON.stringify(data.user));
      window.location.href = "dashboard.html";
    } catch (err) {
      alertBox.textContent = err.message || "Login failed. Please check your credentials.";
      alertBox.classList.remove("d-none");
    } finally {
      btn.disabled = false;
      btnText.textContent = "Login";
      spinner.classList.add("d-none");
    }
  });
}

const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const alertBox = document.getElementById("registerAlert");
    const btn = document.getElementById("registerBtn");
    const btnText = document.getElementById("registerBtnText");
    const spinner = document.getElementById("registerSpinner");

    alertBox.classList.add("d-none");
    if (!name || !email || !password) {
      alertBox.textContent = "Please fill in all fields.";
      alertBox.classList.remove("d-none");
      return;
    }
    if (password.length < 6) {
      alertBox.textContent = "Password must be at least 6 characters.";
      alertBox.classList.remove("d-none");
      return;
    }

    btn.disabled = true;
    btnText.textContent = "Creating account...";
    spinner.classList.remove("d-none");

    try {
      const data = await API.register(name, email, password);
      localStorage.setItem("cc_token", data.token);
      localStorage.setItem("cc_user", JSON.stringify(data.user));
      window.location.href = "dashboard.html";
    } catch (err) {
      alertBox.textContent = err.message || "Registration failed. Please try again.";
      alertBox.classList.remove("d-none");
    } finally {
      btn.disabled = false;
      btnText.textContent = "Sign Up";
      spinner.classList.add("d-none");
    }
  });
}
