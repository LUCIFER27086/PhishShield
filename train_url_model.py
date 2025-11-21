import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os


# Load Dataset

print("Loading URL dataset...")
df = pd.read_csv("phishing_site_urls.csv")   # Replace with actual filename

# Ensure required columns exist
df = df[['URL', 'Label']]
df['URL'] = df['URL'].astype(str)
df['Label'] = df['Label'].astype(int)


# Train-Test Split

X = df['URL']
y = df['Label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Character-Level TF-IDF

print("Extracting TF-IDF features (character-level)...")
tfidf = TfidfVectorizer(
    analyzer='char',
    ngram_range=(3, 5),   # character 3-grams and 5-grams
    max_features=50000
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)


# Train Logistic Regression Model

print("Training URL model...")
model = LogisticRegression(max_iter=2000)
model.fit(X_train_tfidf, y_train)


# Evaluate Model

preds = model.predict(X_test_tfidf)
acc = accuracy_score(y_test, preds)
print("URL Model Accuracy:", acc)
print(classification_report(y_test, preds))


# Save Model + TF-IDF Vectorizer

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/url_model.pkl")
joblib.dump(tfidf, "models/url_tfidf.pkl")

print("\nModel saved as models/url_model.pkl")
print("TF-IDF saved as models/url_tfidf.pkl")
