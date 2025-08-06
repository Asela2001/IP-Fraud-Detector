function checkIP() {
    const ipInput = document.getElementById("ip");
    const resultDiv = document.getElementById("result");
    const loadingDiv = document.getElementById("loading");
    const resultTitle = document.getElementById("result-title");
    const confidenceDiv = document.getElementById("confidence");
    const detailsDiv = document.getElementById("details");
    const errorDiv = document.getElementById("error");

    const ip = ipInput.value.trim();

    // Validate IP format
    const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    if (!ip || !ipRegex.test(ip)) {
        errorDiv.textContent = "Please enter a valid IPv4 address (e.g., 8.8.8.8)";
        errorDiv.style.display = "block";
        resultDiv.style.display = "none";
        return;
    }

    // Clear error and show loading
    errorDiv.style.display = "none";
    loadingDiv.style.display = "block";
    resultDiv.style.display = "none";
    detailsDiv.innerHTML = "";

    // Make API request
    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ip: ip })
    })
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            loadingDiv.style.display = "none";
            resultDiv.style.display = "block";

            if (data.error) {
                resultDiv.className = "";
                resultTitle.textContent = "Error";
                detailsDiv.innerHTML = `<p>${data.error}</p>`;
                errorDiv.textContent = data.error;
                errorDiv.style.display = "block";
                return;
            }

            resultDiv.className = data.fraud ? "fraud" : "safe";
            resultTitle.textContent = data.fraud ? "⚠️ Fraud Risk Detected" : "✓ Safe IP Address";
            const confidencePercent = Math.round(data.probability * 100);
            confidenceDiv.textContent = `Confidence: ${confidencePercent}%`;
            confidenceDiv.className = "confidence " + (confidencePercent < 30 ? "low-risk" : confidencePercent < 70 ? "medium-risk" : "high-risk");

            const details = data.details;
            detailsDiv.innerHTML = `
                <div class="detail-row"><span class="detail-label">IP Address:</span><span>${ip}</span></div>
                <div class="detail-row"><span class="detail-label">Country:</span><span>${details.country}</span></div>
                <div class="detail-row"><span class="detail-label">ISP:</span><span>${details.isp}</span></div>
                <div class="detail-row"><span class="detail-label">Organization:</span><span>${details.org}</span></div>
                <div class="detail-row"><span class="detail-label">Timezone:</span><span>${details.timezone}</span></div>
            `;
        })
        .catch(error => {
            loadingDiv.style.display = "none";
            resultDiv.style.display = "block";
            resultDiv.className = "";
            resultTitle.textContent = "Error";
            detailsDiv.innerHTML = `<p>Error checking IP: ${error.message}</p>`;
            errorDiv.textContent = "An error occurred while checking the IP.";
            errorDiv.style.display = "block";
            console.error("Error:", error);
        });
}

document.getElementById("ip").addEventListener("keypress", function(e) {
    if (e.key === "Enter") checkIP();
});