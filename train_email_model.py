import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import re

print("Loading Email dataset...")

df = pd.read_csv("data/phishing_emails.csv")

# Convert labels: Phishing Email → 1, Safe Email → 0
df['Email Type'] = df['Email Type'].map({
    "Phishing Email": 1,
    "Safe Email": 0
})

# Drop rows with missing labels
df = df.dropna(subset=['Email Type'])

# Clean email text
def clean_email(text):
    text = re.sub(r'<[^>]+>', ' ', str(text))
    text = re.sub(r'http[s]?://\S+', ' ', text)
    text = re.sub(r'[^A-Za-z ]+', ' ', text)
    return text.lower()

df['clean_text'] = df['Email Text'].apply(clean_email)

X = df['clean_text']
y = df['Email Type'].astype(int)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=50000, stop_words='english')
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Logistic Regression model
model = LogisticRegression(max_iter=2000)
model.fit(X_train_tfidf, y_train)

# Predictions
preds = model.predict(X_test_tfidf)
acc = accuracy_score(y_test, preds)

print("\nEmail Model Accuracy:", acc)
print("\nClassification Report:")
print(classification_report(y_test, preds))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/email_model.pkl")
joblib.dump(tfidf, "models/email_tfidf.pkl")

print("\nModel saved to models/ folder.")
