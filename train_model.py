import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import kagglehub
import shutil
import os

# Download dataset
path = kagglehub.dataset_download("alihamzaarain/credit-card-score")

# Move CSV to root folder
for file in os.listdir(path):
    if file.endswith(".csv"):
        shutil.move(os.path.join(path, file), "credit_card_score.csv")
print("Dataset saved to credit_card_score.csv")

# Load dataset
df = pd.read_csv("credit_card_score.csv")

# TODO: Replace with actual column names from credit_card_score.csv
features = ['age','education','income','debtinc','credit_score']
target = 'default'

# Preprocessing
df = df.dropna()
df = pd.get_dummies(df, drop_first=True)
print(df.columns.tolist())
X = df[features]
y = df[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save model and scaler
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
print("Model and scaler saved.")