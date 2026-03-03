const BASE_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", function () {

    console.log("Login JS Loaded");

    const form = document.getElementById("loginForm");
    const loginBtn = document.getElementById("loginBtn");

    // Block default form submission
    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    loginBtn.addEventListener("click", async function () {

        console.log("Login button clicked");

        const messageDiv = document.getElementById("message");
        messageDiv.innerHTML = "Logging in...";
        messageDiv.className = "";

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        try {
            const response = await fetch(BASE_URL + "/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ username, password })
            });

            const data = await response.json(); // ✅ ONLY ONCE

            if (response.ok) {

                console.log("Login successful");

                messageDiv.innerHTML = "Login successful!";
                messageDiv.className = "success";

                // Direct redirect
                window.location.href = data.redirect;

            } else {
                messageDiv.innerHTML = data.error || "Login failed";
                messageDiv.className = "error";
            }

        } catch (error) {
            console.log("Error:", error);
            messageDiv.innerHTML = "Server error";
            messageDiv.className = "error";
        }

    });

});