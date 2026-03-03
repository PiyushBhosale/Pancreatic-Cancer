// ===============================
// SIGNUP SCRIPT - DJANGO SESSION AUTH
// ===============================

const signupForm = document.getElementById("signupForm");
const messageBox = document.getElementById("message");

// -------------------------------
// Get CSRF Token from Cookie
// -------------------------------
function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }

    return cookieValue;
}

// -------------------------------
// Fetch CSRF Token from Backend
// -------------------------------
async function fetchCSRFToken() {
    await fetch("http://127.0.0.1:8000/csrf/", {
        method: "GET",
        credentials: "include"
    });
}

// -------------------------------
// Handle Signup Submit
// -------------------------------
signupForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    messageBox.innerHTML = "Processing...";
    messageBox.className = "";

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
        // Step 1: Get CSRF cookie
        await fetchCSRFToken();

        // Step 2: Read CSRF from cookie
        const csrftoken = getCookie("csrftoken");

        // Step 3: Send POST request
        const response = await fetch("http://127.0.0.1:8000/api/users/", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            messageBox.innerHTML =
                "Registration successful! You can now login.";
            messageBox.className = "success";
            // signupForm.reset(); // clears form fields
        } else {
            messageBox.innerHTML =
                data.detail || JSON.stringify(data);
            messageBox.className = "error";
        }

    } catch (error) {
        console.error("Signup Error:", error);
        messageBox.innerHTML = "Server error. Please try again.";
        messageBox.className = "error";
    }
});