// content.js - The Bridge between Gmail and Python

console.log("🛡️ PhishShield Extension Loaded");

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
        const response = await fetch('http://localhost:5000/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                body: text,
                subject: subject
            })
        });

        const data = await response.json();
        
        // Remove the loader and show real result
        removeBanner(elementToInject);
        injectBanner(data.verdict, data, elementToInject);

    } catch (error) {
        console.error("PhishShield Connection Error:", error);
        removeBanner(elementToInject);
        injectBanner("ERROR", { error: "Is your Python backend running?" }, elementToInject);
    }
}

function removeBanner(container) {
    const existing = container.querySelector('.phish-shield-banner');
    if (existing) existing.remove();
}

function injectBanner(status, data, container) {
    const banner = document.createElement('div');
    banner.className = `phish-shield-banner ps-${status.toLowerCase()}`;
    
    let htmlContent = '';

    if (status === "LOADING") {
        htmlContent = `
            <div class="ps-spinner"></div>
            <span><strong>PhishShield:</strong> Analyzing email with Python AI...</span>
        `;
    } else if (status === "ERROR") {
        htmlContent = `
            <span><strong>⚠️ Connection Failed:</strong> Ensure server.py is running!</span>
        `;
    } else if (status === "SAFE") {
        htmlContent = `
            <div class="ps-icon">🛡️</div>
            <div>
                <strong>VERIFIED SAFE</strong><br>
                <small>No suspicious patterns detected.</small>
            </div>
        `;
    } else {
        // Suspicious or Dangerous
        htmlContent = `
            <div class="ps-icon">💀</div>
            <div>
                <strong>${status} DETECTED (${data.score}% Risk)</strong><br>
                <small>${data.reasons.join(', ')}</small>
            </div>
        `;
    }

    banner.innerHTML = htmlContent;
    container.prepend(banner);
}