from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import sqlite3

app = Flask(__name__)
CORS(app)

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/styles.css')
def serve_css():
    return send_file('styles.css')

@app.route('/script.js')
def serve_js():
    return send_file('script.js')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data
        data = request.get_json()
        input_data = pd.DataFrame([{
            'income': float(data['income']),
            'debtinc': float(data['debtinc']),
            'credit_score': float(data['credit_score']),
            'age': float(data['age']),
            'education': float(data['education'])
        }])

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_scaled)[0]
        result = 'Creditworthy' if prediction == 1 else 'Not Creditworthy'

        # Save to SQLite
        conn = sqlite3.connect('credit_score.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                income FLOAT,
                debtinc FLOAT,
                credit_score FLOAT,
                age FLOAT,
                education FLOAT,
                prediction TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            INSERT INTO predictions(income, debtinc, credit_score, age, education, prediction)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['income'], data['debtinc'], data['credit_score'], data['age'], data['education'], result))
        conn.commit()
        conn.close()

        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)