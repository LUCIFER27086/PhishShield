# 🛡️ PhishShield – AI-Powered URL & Email Phishing Detection System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Cybersecurity](https://img.shields.io/badge/Domain-Cybersecurity-green)
![ML](https://img.shields.io/badge/ML-LogisticRegression-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

---

## 📌 Overview

**PhishShield** is an **AI + heuristic–based cybersecurity tool** that detects phishing URLs and phishing emails using:

- Machine Learning (TF-IDF + Logistic Regression)
- Heuristic (rule-based) analysis
- NLP-based sentiment & keyword detection
- Hybrid scoring system (ML 60% + Heuristic 40%)
- Risk visualization (matplotlib)

This project was built as part of the **UE25CS151A – Python for Computational Problem Solving** mini-project.

PhishShield achieves **90–95% accuracy** using real phishing datasets from Kaggle.

---

## 🎯 Features

### 🔐 URL Phishing Detection
- Character-level TF-IDF  
- Logistic Regression (92–95% accuracy)  
- Detects:  
  ✔ IP-based URLs  
  ✔ Suspicious patterns (verify, login, update)  
  ✔ Encoding (%20, %3A)  
  ✔ Hyphen & dot abuse  
  ✔ Long URLs  
  ✔ Suspicious subdomains  
  ✔ Non-HTTPS URLs  

---

### ✉️ Email Phishing Detection
- Word-level TF-IDF  
- Logistic Regression (90–93% accuracy)  
- NLP-based Analysis:  
  ✔ Urgency detection  
  ✔ Threat tone (sentiment polarity)  
  ✔ Suspicious keywords  
  ✔ HTML content  
  ✔ Link count  
  ✔ Spoofed sender patterns  

---

### 🧠 Hybrid Scoring
```
Final Score = 60% (ML probability) + 40% (heuristic score)
```

Output:
- ML probability of phishing  
- Final risk score (0–100%)  
- Verdict: Safe / Suspicious / Dangerous  
- Visualization graph  

---

## 📂 Folder Structure

```
PhishShield/
│
├── main.py
├── features.py
│
├── train_url_model.py
├── train_email_model.py
│
├── models/
│   ├── email_model.pkl
│   ├── email_tfidf.pkl
│
├── screenshots/
│   ├── console_output.png
│   ├── risk_chart.png
│   ├── email_sample.png
│
├── data/
│   ├── phishing_emails.csv
│
├── docs/
│   ├── PhishShield_Project_Report.docx
│   ├── architecture.png
│   ├── system_flowchart.png
│
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/<your-team-name>/PhishShield.git
cd PhishShield
pip install -r requirements.txt
```

Download required TextBlob corpora:
```bash
python -m textblob.download_corpora
```

---

## 🤖 Training the Machine Learning Models

### **1️⃣ Train URL Model(Currently not trained)**
```bash
python train_url_model.py
```
This generates:
```
models/url_model.pkl
models/url_tfidf.pkl
```

---

### **2️⃣ Train Email Model**
```bash
python train_email_model.py
```
This generates:
```
models/email_model.pkl
models/email_tfidf.pkl
```

---

## 🚀 Running PhishShield

Run the system using:
```bash
python main.py
```

Examples you can test:

### URL Input:
```
http://paypa1-secure-verify-login.com/update
```

### Email Input:
```
Your account has been suspended! Verify immediately at:
http://secure-pay-update.com/login
```

The output includes:
- ML probability  
- Final hybrid score  
- Risk classification  
- Visualization graph saved at:

```
screenshots/risk_chart.png
```

---

## 🧠 System Architecture

```
Input (URL/Email)
       ↓
Heuristic Feature Extractor
       ↓
TF-IDF Vectorizer (URL/Email)
       ↓
ML Model (Logistic Regression)
       ↓
Hybrid Risk Score (ML + Heuristics)
       ↓
Visualization + Verdict
```

---

## 📊 Screenshots

- screenshots/console_output.png  
- screenshots/risk_chart.png  
- screenshots/email_sample.png  

---

## 👥 Contributors

| Name | Role |
|------|------|
| Sameer Manvi | ML + Heuristics |
| Pratheek GN | Visualization + Testing |
| Samruddhi | Documentation + Report |
| Rohith  | Repo + Integration |

---

## 📚 Datasets Used

### URL Dataset  
**Phishing Website Dataset (A3 – Kaggle)**

### Email Dataset  
**Phishing Emails Dataset (B1 – Kaggle)**


## © License

This project is for educational and academic use only.
