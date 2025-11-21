import re
import tldextract
from textblob import TextBlob
import joblib
import numpy as np
import matplotlib.pyplot as plt


# Load ML Models

url_model = joblib.load("models/url_model.pkl")
url_tfidf = joblib.load("models/url_tfidf.pkl")

email_model = joblib.load("models/email_model.pkl")
email_tfidf = joblib.load("models/email_tfidf.pkl")



# URL Feature Extraction (heuristics)

def analyze_url(url):
    features = {}

    # IP-based detection
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'
    features['ip_based'] = bool(re.search(ip_pattern, url))

    extracted = tldextract.extract(url)
    domain = extracted.domain
    subdomain = extracted.subdomain
    suffix = extracted.suffix

    features['domain'] = domain
    features['subdomain'] = subdomain
    features['suffix'] = suffix

    features['num_dots'] = url.count('.')

    suspicious_words = ['login', 'verify', 'update', 'secure', 'banking', 'account']
    features['suspicious_words'] = any(word in url.lower() for word in suspicious_words)

    features['num_hyphens'] = url.count('-')
    features['url_length'] = len(url)
    features['encoded_chars'] = '%' in url
    features['https'] = url.startswith("https://")
    features['subdomain_count'] = len(subdomain.split('.')) if subdomain else 0

    return features



# Email Feature Extraction (heuristics)

def analyze_email(text):
    features = {}
    clean_text = text.lower()

    urgency_words = ['urgent', 'immediately', 'suspended', 'verify', 'alert', 'warning']
    features['urgent_words'] = any(word in clean_text for word in urgency_words)

    phishing_words = ['password', 'bank', 'update', 'security', 'click here', 'confirm']
    features['phishing_words'] = any(word in clean_text for word in phishing_words)

    url_regex = r'(http[s]?://[^\s]+)'
    features['link_count'] = len(re.findall(url_regex, text))

    features['sentiment'] = TextBlob(text).sentiment.polarity

    html_regex = r'<[^>]+>'
    features['contains_html'] = bool(re.search(html_regex, text))

    features['exclamation_count'] = clean_text.count('!')

    spoof_regex = r'from:\s.*@(?!gmail\.com|yahoo\.com|outlook\.com)'
    features['possible_spoof'] = bool(re.search(spoof_regex, clean_text))

    features['word_count'] = len(clean_text.split())

    return features



# ML Predictions

def predict_url_ml(url):
    vector = url_tfidf.transform([url])
    prob = url_model.predict_proba(vector)[0][1]  # probability phishing
    return prob


def predict_email_ml(text):
    vector = email_tfidf.transform([text])
    prob = email_model.predict_proba(vector)[0][1]  # probability phishing
    return prob



# Hybrid Score: ML + Heuristics

def calculate_score(features, ml_probability):
    # Heuristic score
    h_score = 0

    if features.get('ip_based'): h_score += 20
    if features.get('suspicious_words'): h_score += 15
    if features.get('num_dots', 0) > 3: h_score += 10
    if features.get('num_hyphens', 0) > 4: h_score += 10
    if features.get('encoded_chars'): h_score += 10
    if not features.get('https'): h_score += 20
    if features.get('urgent_words'): h_score += 20
    if features.get('phishing_words'): h_score += 15
    if features.get('link_count', 0) > 2: h_score += 10
    if features.get('sentiment', 0) < -0.3: h_score += 10
    if features.get('contains_html'): h_score += 10

    # Normalize heuristic score to 0–100
    h_score = min(h_score, 100)

    # Hybrid Score
    final_score = (0.6 * (ml_probability * 100)) + (0.4 * h_score)
    final_score = min(final_score, 100)

    # Verdict
    if final_score < 30:
        verdict = "Safe"
    elif final_score < 60:
        verdict = "Suspicious"
    else:
        verdict = "Dangerous"

    return final_score, verdict



# Visualization

def visualize_result(features, score, verdict):
    keys = list(features.keys())
    values = [int(v) if isinstance(v, bool) else v for v in features.values()]

    plt.figure(figsize=(8, 5))
    plt.barh(keys, values)
    plt.title(f"PhishShield Risk Analysis\nScore: {round(score,2)}% - Verdict: {verdict}")
    plt.tight_layout()
    plt.savefig("screenshots/risk_chart.png")
