document.addEventListener("DOMContentLoaded", function () {
    // 🔹 Password Show/Hide Toggle
    const passwordField = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");

    togglePassword.addEventListener("click", function () {
        if (passwordField.type === "password") {
            passwordField.type = "text";
            togglePassword.classList.remove("fa-eye");
            togglePassword.classList.add("fa-eye-slash");
        } else {
            passwordField.type = "password";
            togglePassword.classList.remove("fa-eye-slash");
            togglePassword.classList.add("fa-eye");
        }
    });

    // 🔹 Continue Button Enable/Disable Logic
    const usernameField = document.getElementById("username");
    const continueBtn = document.querySelector(".btn");
    const form = document.querySelector("form");

    function validateFields() {
        if (usernameField.value.trim() !== "" && passwordField.value.trim() !== "") {
            continueBtn.removeAttribute("disabled");
        } else {
            continueBtn.setAttribute("disabled", "true");
        }
    }

    usernameField.addEventListener("input", validateFields);
    passwordField.addEventListener("input", validateFields);

    // 🔹 Status Message Box
    const statusBox = document.createElement("div");
    statusBox.id = "loginStatus";
    statusBox.style.display = "none";
    statusBox.style.marginTop = "10px";
    statusBox.style.padding = "10px";
    statusBox.style.textAlign = "center";
    statusBox.style.borderRadius = "5px";
    form.appendChild(statusBox);

    // 🔹 Form Submit Event
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        continueBtn.setAttribute("disabled", "true"); // Disable immediately after submit

        const username = usernameField.value.trim();
        const password = passwordField.value.trim();

        fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Server Response:", data);

            if (data.success) {
                statusBox.textContent = "Login successful!";
                statusBox.style.backgroundColor = "green";
                statusBox.style.color = "white";
            } else {
                statusBox.textContent = "Sorry incorrect password";
                statusBox.style.backgroundColor = "red";
                statusBox.style.color = "white";
            }

            statusBox.style.display = "block";
            form.reset();
            continueBtn.setAttribute("disabled", "true");

            // 🔹 Auto-hide status message after 3 seconds
            setTimeout(() => {
                statusBox.style.display = "none";
            }, 3000);
        })
        .catch(error => {
            console.error("Error:", error);
            statusBox.textContent = "Error submitting data!";
            statusBox.style.backgroundColor = "red";
            statusBox.style.color = "white";
            statusBox.style.display = "block";

            setTimeout(() => {
                statusBox.style.display = "none";
            }, 3000);
        });
    });
});
