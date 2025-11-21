import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("Loading URL dataset...")

# Load dataset
df = pd.read_csv("data/phishing_site_urls.csv")

# Features = all columns except 'Result'
X = df.drop(columns=['Result'])

# Label = 'Result'
y = df['Result']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Random Forest Model (BEST for this dataset)
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=None,
    random_state=42
)

print("Training URL model...")
model.fit(X_train, y_train)

# Predictions
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)

print("\nURL Model Accuracy:", acc)
print("\nClassification Report:")
print(classification_report(y_test, preds))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/url_model.pkl")

print("\nModel saved as models/url_model.pkl")
