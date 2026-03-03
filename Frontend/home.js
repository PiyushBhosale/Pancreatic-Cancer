const BASE_URL = "http://127.0.0.1:8000";

// Check session authentication
window.onload = function() {
    fetch(BASE_URL + "/check-auth/", {
        method: "GET",
        credentials: "include"
    })
    .then(response => {
        if (!response.ok) {
            window.location.href = "login.html";
        }
    })
    .catch(() => {
        window.location.href = "login.html";
    });
};

// Logout function
function logout() {
    fetch(BASE_URL + "/logout/", {
        method: "POST",
        credentials: "include"
    })
    .then(() => {
        window.location.href = "login.html";
    });
}