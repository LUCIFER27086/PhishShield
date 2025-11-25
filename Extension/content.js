// content.js - The Bridge between Gmail and Python

console.log("🛡️ PhishShield Extension Loaded");

// Target for the Python server (MUST use 127.0.0.1 to match manifest permissions)
const SERVER_URL = 'http://127.0.0.1:5000/scan';

// We need to wait for Gmail to render the email body.
// We use a MutationObserver to watch the DOM.
const observer = new MutationObserver((mutations) => {
    // '.a3s.aiL' is the specific class Gmail uses for the email body container
    const emailBodies = document.querySelectorAll('.a3s.aiL'); 
    // '.hP' is often the class for the Subject line in the open view
    const subjectLine = document.querySelector('h2.hP'); 

    emailBodies.forEach((emailBody) => {
        // Only scan if we haven't scanned this specific email view yet
        if (!emailBody.getAttribute('data-ps-scanned')) {
            emailBody.setAttribute('data-ps-scanned', 'true'); // Mark as scanned

            const text = emailBody.innerText;
            const subject = subjectLine ? subjectLine.innerText : "Unknown Subject";

            // Send to Python Backend
            scanWithPython(text, subject, emailBody);
        }
    });
});

// Start watching the page
observer.observe(document.body, { childList: true, subtree: true });

async function scanWithPython(text, subject, elementToInject) {
    // Show a "Scanning..." loader
    injectBanner("LOADING", {}, elementToInject);

    try {
        const response = await fetch(SERVER_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                body: text,
                subject: subject
            })
        });

        // Check for non-200 responses (e.g., 500 error from Flask)
        if (!response.ok) {
            // Throw an error that gets caught below
            throw new Error(`Server responded with status: ${response.status}`);
        }

        const data = await response.json();
        
        // Remove the loader and show real result
        removeBanner(elementToInject);
        injectBanner(data.verdict, data, elementToInject);

    } catch (error) {
        // Updated error message to be more informative
        console.error("PhishShield Connection Error:", error);
        removeBanner(elementToInject);
        injectBanner("ERROR", { error: error.message || "Ensure server is running and URLs match." }, elementToInject);
    }
}

/**
 * Helper function to remove the existing banner element.
 */
function removeBanner(container) {
    const existing = container.querySelector('.phish-shield-banner');
    if (existing) existing.remove();
}

/**
 * Helper function to create and inject the status banner into the email body.
 */
function injectBanner(status, data, container) {
    const banner = document.createElement('div');
    // Ensure status is uppercase for consistent class naming
    const statusClass = status.toUpperCase();
    banner.className = `phish-shield-banner ps-${statusClass.toLowerCase()}`;
    
    let htmlContent = '';

    if (statusClass === "LOADING") {
        htmlContent = `
            <div class="ps-spinner"></div>
            <span><strong>PhishShield:</strong> Analyzing email with Heuristic Scanner...</span>
        `;
    } else if (statusClass === "ERROR") {
        htmlContent = `
            <div class="ps-icon">❌</div>
            <span><strong>⚠️ Connection Failed:</strong> Is your Python backend running? Details: ${data.error || 'Check browser console.'}</span>
        `;
    } else if (statusClass === "SAFE") {
        htmlContent = `
            <div class="ps-icon">🛡️</div>
            <div>
                <strong>VERIFIED SAFE</strong><br>
                <small>No suspicious patterns detected.</small>
            </div>
        `;
    } else {
        // SUSPICIOUS or DANGEROUS
        const icon = statusClass === "DANGEROUS" ? '💀' : '⚠️';
        const riskScore = data.score !== undefined ? data.score.toFixed(0) : 'N/A';
        const reasonsList = data.reasons && data.reasons.length > 0 ? data.reasons.join(', ') : 'Heuristic analysis triggered.';

        htmlContent = `
            <div class="ps-icon">${icon}</div>
            <div>
                <strong>${statusClass} DETECTED (${riskScore}% Risk)</strong><br>
                <small>Reasons: ${reasonsList}</small>
            </div>
        `;
    }

    banner.innerHTML = htmlContent;
    // Prepend (add to the top) of the email container
    container.prepend(banner);
}