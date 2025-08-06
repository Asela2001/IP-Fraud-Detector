function checkIP() {
  const ipInput = document.getElementById('ip');
  const resultDiv = document.getElementById('result');
  const loadingDiv = document.getElementById('loading');
  const resultTitle = document.getElementById('result-title');
  const confidenceDiv = document.getElementById('confidence');
  const detailsDiv = document.getElementById('details');
  
  const ip = ipInput.value.trim();
  
  // Basic IP validation
  if (!ip) {
    alert('Please enter an IP address');
    return;
  }
  
  // Show loading indicator
  loadingDiv.style.display = 'block';
  resultDiv.style.display = 'none';
  
  // Clear previous results
  detailsDiv.innerHTML = '';
  
  // Make API request
  fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ ip: ip })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Hide loading indicator
    loadingDiv.style.display = 'none';
    
    // Display results
    resultDiv.style.display = 'block';
    
    if (data.error) {
      resultDiv.className = '';
      resultTitle.textContent = 'Error';
      detailsDiv.innerHTML = `<p>${data.error}</p>`;
      return;
    }
    
    // Set result styling based on fraud detection
    if (data.fraud) {
      resultDiv.className = 'fraud';
      resultTitle.textContent = '⚠️ Fraud Risk Detected';
    } else {
      resultDiv.className = 'safe';
      resultTitle.textContent = '✓ Safe IP Address';
    }
    
    // Set confidence level with appropriate styling
    const confidencePercent = Math.round(data.probability * 100);
    confidenceDiv.textContent = `Confidence: ${confidencePercent}%`;
    
    if (confidencePercent < 30) {
      confidenceDiv.className = 'confidence low-risk';
    } else if (confidencePercent < 70) {
      confidenceDiv.className = 'confidence medium-risk';
    } else {
      confidenceDiv.className = 'confidence high-risk';
    }
    
    // Display IP details
    const details = data.details;
    detailsDiv.innerHTML = `
      <div class="detail-row">
        <span class="detail-label">IP Address:</span>
        <span>${ip}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Country:</span>
        <span>${details.country}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">ISP:</span>
        <span>${details.isp}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Organization:</span>
        <span>${details.org}</span>
      </div>
      <div class="detail-row">
        <span class="detail-label">Timezone:</span>
        <span>${details.timezone}</span>
      </div>
    `;
  })
  .catch(error => {
    loadingDiv.style.display = 'none';
    resultDiv.style.display = 'block';
    resultDiv.className = '';
    resultTitle.textContent = 'Error';
    detailsDiv.innerHTML = `<p>Error checking IP: ${error.message}</p>`;
    console.error('Error:', error);
  });
}

// Allow pressing Enter key to submit
document.getElementById('ip').addEventListener('keypress', function(e) {
  if (e.key === 'Enter') {
    checkIP();
  }
});