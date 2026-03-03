const BASE_URL = "http://127.0.0.1:8000";

// Check authentication
window.onload = function() {
    fetch(BASE_URL + "/check-auth/", {
        method: "GET",
        credentials: "include"
    })
    .then(response => {
        if (!response.ok) {
            window.location.href = "login.html";
        } else {
            loadHistory();
        }
    })
    .catch(() => {
        window.location.href = "login.html";
    });
};

// Logout
function logout() {
    fetch(BASE_URL + "/logout/", {
        method: "POST",
        credentials: "include"
    })
    .then(() => {
        window.location.href = "login.html";
    });
}

// Make Prediction
function makePrediction() {
    const fileInput = document.getElementById("imageInput");
    const loader = document.getElementById("loader");
    const resultDiv = document.getElementById("result");

    if (!fileInput.files.length) {
        alert("Please upload an image.");
        return;
    }

    const formData = new FormData();
    formData.append("uploaded_image", fileInput.files[0]);

    loader.classList.remove("hidden");
    resultDiv.innerHTML = "";

    fetch(BASE_URL + "/api/cancer/", {
        method: "POST",
        credentials: "include",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        loader.classList.add("hidden");

        const confidencePercent = (data.confidence_score).toFixed(2);

        let resultClass = data.predicted_label === "Cancer" ? "cancer" : "normal";

        resultDiv.innerHTML = `
            <div class="result-box ${resultClass}">
                Result: ${data.predicted_label} <br>
                Confidence: ${confidencePercent}%
                <div class="progress-container">
                    <div class="progress-bar" style="width:${confidencePercent}%"></div>
                </div>
            </div>
        `;

        loadHistory();
    })
    .catch(() => {
        loader.classList.add("hidden");
        resultDiv.innerHTML = "Error processing image.";
    });
}

// Load History
function loadHistory() {
    fetch(BASE_URL + "/api/cancer/", {
        method: "GET",
        credentials: "include"
    })
    .then(res => res.json())
    .then(data => {
        const historyDiv = document.getElementById("history");
        historyDiv.innerHTML = "";

        data.forEach(item => {
            const confidencePercent = (item.confidence_score).toFixed(2);

            historyDiv.innerHTML += `
                <div class="history-item">
                    ${item.predicted_label} |
                    Confidence: ${confidencePercent}% |
                    Date: ${new Date(item.created_at).toLocaleString()}
                </div>
            `;
        });
    });
}