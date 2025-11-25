from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin # IMPORTANT: Make sure cross_origin is imported
from textblob import TextBlob
import re
import json

# Initialize the Flask App
app = Flask(__name__)
# Enable CORS for the entire application (safer for local development)
CORS(app) 

print("🛡️ PhishShield AI Server is Starting...")

# --- 1. Test Route for Debugging (GET request to check if server is running) ---
@app.route('/', methods=['GET'])
def home():
    # This route is only for verifying the server is up and running.
    return jsonify({"status": "PhishShield Server is running and healthy!", "version": "2.0"}), 200

# --- 2. THE DETECTION LOGIC (Simplified for Demo) ---
# NOTE: Replace this with your actual ML model loading and prediction logic later!

def analyze_risk(text, subject):
    score = 0
    reasons = []
    
    # Combine subject and body for analysis
    full_text = f"{subject} {text}".lower()

    # A. Urgency Detection (Social Engineering)
    urgent_patterns = [
        "immediately", "action required", "suspended", "verify your account",
        "24 hours", "urgently", "unauthorized access"
    ]
    for word in urgent_patterns:
        if word in full_text:
            score += 20
            reasons.append(f"Urgency detected: '{word}'")

    # B. Suspicious Links (Heuristic)
    # Check for links that don't match the text (e.g., "paypal" text linking to "bit.ly")
    if "bit.ly" in full_text or "tinyurl" in full_text:
        score += 15
        reasons.append("Hidden/Shortened URL detected")

    # C. Sentiment Analysis (NLP)
    # Phishing emails often use aggressive or fear-inducing language (Negative Polarity)
    blob = TextBlob(full_text)
    if blob.sentiment.polarity < -0.1:
        score += 10
        reasons.append("Negative/Threatening tone detected")

    # D. Sensitive Keyword Targeting
    sensitive_words = ["password", "credit card", "bank account", "social security", "ssn"]
    for word in sensitive_words:
        if word in full_text:
            score += 25
            reasons.append(f"Asking for sensitive info: '{word}'")

    # Cap score at 100
    total_risk = min(score, 100)
    
    # Determine Verdict
    if total_risk < 30:
        verdict = "SAFE"
    elif total_risk < 70:
        verdict = "SUSPICIOUS"
    else:
        verdict = "DANGEROUS"

    return {
        "score": total_risk,
        "verdict": verdict,
        "reasons": list(set(reasons)) # Remove duplicates
    }

# --- 3. THE API ENDPOINT (Main scanning route) ---
@app.route('/scan', methods=['POST'])
@cross_origin() # <--- THIS IS THE FIX FOR THE CONNECTION ERROR
def scan_email():
    try:
        # Flask handles reading the JSON body from the POST request
        data = request.json
        
        # Simple validation
        if not data or 'body' not in data:
            return jsonify({"error": "Missing 'body' data in request."}), 400
            
        email_text = data.get('body', '')
        email_subject = data.get('subject', 'No Subject')

        print(f"🔎 Scanning email: {email_subject[:30]}...")
        
        result = analyze_risk(email_text, email_subject)
        
        return jsonify(result)

    except Exception as e:
        print(f"Server Error during scan: {e}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the server on localhost port 5000
    # Use 127.0.0.1 for maximum compatibility with localhost setup
    app.run(host='127.0.0.1', port=5000, debug=True)