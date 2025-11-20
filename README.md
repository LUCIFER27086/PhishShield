![Python](https://img.shields.io/badge/Python-3.10-blue)
![Cybersecurity](https://img.shields.io/badge/Domain-Cybersecurity-green)
![Status](https://img.shields.io/badge/Status-Complete-success)

# 🛡️ PhishShield – Intelligent Email and URL Phishing Detection System


## 🧠 Overview
PhishShield is a cybersecurity project designed to detect phishing attempts using a multi-layered approach.
It analyzes URLs and email content using structural, linguistic, and sentiment-based techniques to determine the probability of phishing.

## ⚙️ Features
- URL structure analysis (detects IPs, subdomains, encoded links)
- Linguistic analysis (detects urgency words, spoofed senders)
- Sentiment-based tone detection
- Risk scoring system with visualization
- Log file for tracking analysis
- (Optional) ML-based classifier for phishing prediction

## 🧩 Tech Stack
- Python 3.x
- Libraries: `re`, `tldextract`, `textblob`, `matplotlib`, `pandas`, `csv`

## 🧱 Folder Structure
```
PhishShield/
├── main.py
├── features.py
├── phishing_samples.csv
├── results.csv
├── screenshots/
│   ├── console_output.png
│   ├── risk_chart.png
└── README.md
```

## 🚀 Execution
1. Clone the repository:
   ```bash
   git clone https://github.com/sameermanvi/PhishShield.git
   cd PhishShield
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python main.py
   ```

4. View results:
   - Risk score printed in console
   - Visualization image saved as `.png`
   - Log file updated in `results.csv`

## 📊 Example Output
```
Analyzing email: "Your PayPal account has been locked. Verify now at paypa1-login.com"
---------------------------------------------------
⚠️ Phishing Probability: 86%
Key Indicators:
- Urgent tone detected
- Suspicious URL pattern
- Spoofed domain
Verdict: DANGEROUS
---------------------------------------------------
```

## 🧩 Contributors
| Name | Role |
|------|------|
| Rohith Balasubramanya | Team Lead |
| Pratheek G N | Visualization Developer |
| Sameer Manvi | NLP & Feature Engineer |
| Samruddhi Shyamkant | Documentation & Testing |

## 📚 License
This project is for academic and research use only.

## 🗓️ Project Progress

- [x] Folder structure & README  
- [x] Project report (DOCX)  
- [x] Added main.py and features.py skeleton  
- [x] Implement analyze_url()  
- [ ] Implement analyze_email()  
- [ ] Implement calculate_score()  
- [ ] Add visualization (matplotlib)  
- [ ] Add logging to results.csv  
- [ ] Final testing with sample URLs  
- [ ] Add screenshots to README & Report  
- [ ] Freeze final submission  
