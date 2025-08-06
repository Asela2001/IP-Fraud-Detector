from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import requests
import joblib
import pickle
import numpy as np
import sqlite3
from datetime import datetime

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your_secret_key_123'  # Change to a secure random key in production

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('ip_checks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ip_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL,
            prediction TEXT NOT NULL,
            probability REAL NOT NULL,
            country TEXT,
            isp TEXT,
            org TEXT,
            timezone TEXT,
            flagged BOOLEAN DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Check if model and encoder files exist in the model folder
model_path = os.path.join("model", "ip_fraud_detection_model.pkl")
encoder_path = os.path.join("model", "label_encoders.pkl")
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found in backend/model directory")
if not os.path.exists(encoder_path):
    raise FileNotFoundError(f"Encoder file '{encoder_path}' not found in backend/model directory")

# Load the model and encoders
try:
    model = joblib.load(model_path)
    with open(encoder_path, "rb") as f:
        label_encoders = pickle.load(f)
except Exception as e:
    print(f"Error loading model or encoders: {e}")
    raise

def extract_ip_features(ip):
    """Extract numerical features from IP address"""
    try:
        parts = list(map(int, ip.split('.')))
        return {
            'ip_first_octet': parts[0],
            'ip_second_octet': parts[1],
            'ip_third_octet': parts[2],
            'ip_fourth_octet': parts[3]
        }
    except:
        return {
            'ip_first_octet': 0,
            'ip_second_octet': 0,
            'ip_third_octet': 0,
            'ip_fourth_octet': 0
        }

def fetch_ip_info(ip):
    """Fetch IP information from ip-api.com"""
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,isp,org,timezone")
        data = res.json()
        if data.get('status') == 'fail':
            return {"country": "Unknown", "isp": "Unknown", "org": "Unknown", "timezone": "Unknown"}
        return {
            "country": data.get("country", "Unknown"),
            "isp": data.get("isp", "Unknown"),
            "org": data.get("org", "Unknown"),
            "timezone": data.get("timezone", "Unknown")
        }
    except Exception as e:
        print(f"Error fetching IP info: {e}")
        return {"country": "Unknown", "isp": "Unknown", "org": "Unknown", "timezone": "Unknown"}

def prepare_features(ip, ip_info):
    """Prepare features for model prediction"""
    ip_features = extract_ip_features(ip)
    encoded_features = {}
    for col in ['country', 'org', 'isp', 'timezone']:
        try:
            le = label_encoders[col]
            encoded_val = le.transform([ip_info[col]])[0] if ip_info[col] in le.classes_ else 0
            encoded_features[col] = encoded_val
        except Exception as e:
            print(f"Error encoding {col}: {e}")
            encoded_features[col] = 0
    features = [
        ip_features['ip_first_octet'],
        ip_features['ip_second_octet'],
        ip_features['ip_third_octet'],
        ip_features['ip_fourth_octet'],
        encoded_features['country'],
        encoded_features['org'],
        encoded_features['isp'],
        encoded_features['timezone']
    ]
    return np.array([features])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    ip = data.get("ip")
    if not ip:
        return jsonify({"error": "IP address not provided"}), 400
    ip_info = fetch_ip_info(ip)
    try:
        features = prepare_features(ip, ip_info)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        # Save to database
        conn = sqlite3.connect('ip_checks.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO ip_checks (ip, prediction, probability, country, isp, org, timezone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (ip, 'Fraud' if prediction == 1 else 'Safe', probability,
              ip_info['country'], ip_info['isp'], ip_info['org'], ip_info['timezone']))
        conn.commit()
        conn.close()
        return jsonify({
            "fraud": bool(prediction),
            "probability": float(probability),
            "details": ip_info
        })
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": "Could not process the IP address", "details": str(e)}), 500

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Replace with secure authentication in production
        if username == "admin" and password == "password":
            session["logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html", error=None)

@app.route("/admin/logout")
def admin_logout():
    session.pop("logged_in", None)
    return redirect(url_for("admin_login"))

def requires_login(f):
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/admin/dashboard")
@requires_login
def admin_dashboard():
    conn = sqlite3.connect('ip_checks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ip_checks ORDER BY timestamp DESC")
    ip_checks = c.fetchall()
    c.execute("SELECT COUNT(*) FROM ip_checks WHERE prediction = 'Safe'")
    safe_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM ip_checks WHERE prediction = 'Fraud'")
    fraud_count = c.fetchone()[0]
    conn.close()
    return render_template("dashboard.html", ip_checks=ip_checks, safe_count=safe_count, fraud_count=fraud_count)

@app.route("/admin/flag/<int:ip_id>", methods=["POST"])
@requires_login
def flag_ip(ip_id):
    conn = sqlite3.connect('ip_checks.db')
    c = conn.cursor()
    c.execute("UPDATE ip_checks SET flagged = NOT flagged WHERE id = ?", (ip_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)