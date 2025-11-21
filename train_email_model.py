import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import re


# Load Dataset

print("Loading Email dataset...")
df = pd.read_csv("phishing_emails.csv")  # Replace with actual filename

# Combine subject + body if separate
if "Email Text" in df.columns:
    df['text'] = df["Email Text"].astype(str)
elif "Body" in df.columns:
    df['text'] = df["Body"].astype(str)
else:
    df['text'] = df.iloc[:, 0].astype(str)

df['Label'] = df['Label'].astype(int)


# Clean Email Text

def clean_email(text):
    text = re.sub(r'<[^>]+>', ' ', text)        # remove HTML tags
    text = re.sub(r'http[s]?://\S+', ' ', text) # remove URLs
    text = re.sub(r'[^A-Za-z ]+', ' ', text)    # keep only words
    return text.lower()

df['clean_text'] = df['text'].apply(clean_email)


# Train-Test Split

X = df['clean_text']
y = df['Label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# TF-IDF (Word-Level)

print("Extracting TF-IDF features (word-level)...")
tfidf = TfidfVectorizer(
    max_features=50000,
    stop_words='english'
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)


# Train Model

print("Training Email model...")
model = LogisticRegression(max_iter=2000)
model.fit(X_train_tfidf, y_train)


# Evaluate

preds = model.predict(X_test_tfidf)
acc = accuracy_score(y_test, preds)
print("Email Model Accuracy:", acc)
print(classification_report(y_test, preds))


# Save Model + TF-IDF Vectorizer

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/email_model.pkl")
joblib.dump(tfidf, "models/email_tfidf.pkl")

print("\nModel saved as models/email_model.pkl")
print("TF-IDF saved as models/email_tfidf.pkl")
