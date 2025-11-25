# UE25CS151A
# PhishShield – Phishing Email Detection System

PhishShield is a lightweight phishing-email detection tool that connects a Python backend with a Chrome extension to scan Gmail emails in real time. It analyzes email content using heuristic rules and shows a safety banner directly inside Gmail.

## Project Structure
   
    PhishShield/
    │
    ├── Backend/
    │   └── server.py
    │
    └── Extension/
        ├── content.js
        ├── manifest.json
        └── styles.css
    
## How It Works
1. The Chrome extension observes Gmail when an email is opened.
2. It extracts the email subject and body.
3. It sends the data to the Python backend at /scan.
4. The backend analyzes the text and returns SAFE, SUSPICIOUS, or DANGEROUS.
5. A colored banner is shown at the top of the email.

## Run the Backend
Install dependencies:
pip install -r requirements.txt

Start the server:
python server.py

Backend runs on:
http://127.0.0.1:5000

## Load the Chrome Extension
1. Open Chrome and go to chrome://extensions/
2. Enable Developer Mode
3. Click Load Unpacked
4. Select the Extension/ folder

## Features
- Real-time Gmail scanning
- Heuristic phishing detection
- Score-based risk evaluation
- Clean UI banners (safe, suspicious, dangerous)
- Lightweight and fast

## Requirements
- Python 3.x
- Flask
- flask-cors
- TextBlob

## Authors
PhishShield Development Team
-|Sameer Manvi | PES2UG25CS725
-|Pratheek G N |PES2UG25EC097
-|Rohith B | PES2UG25EC104|
