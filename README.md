🕵️‍♂️ IP Fraud Detection System
A web-based solution to detect potentially fraudulent IP addresses using machine learning and real-time geolocation data.

📌 Project Overview
This project implements an IP Fraud Detection System with:

✅ A trained RandomForestClassifier model

🌐 A Flask web application

🔐 An Admin Panel for managing and monitoring IP checks

📡 Integration with ip-api.com for IP geolocation data

Admins can view reports, flag suspicious IPs, and visualize prediction trends via an interactive dashboard.

🚀 Setup Instructions
✅ Prerequisites
🐍 Python 3.8+

🧬 Git

📥 Installation
Clone the Repository


git clone https://github.com/your-username/ip-fraud-detector.git
cd ip-fraud-detector

Create a Virtual Environment


python -m venv venv
Activate the Environment

Windows (PowerShell):

.\venv\Scripts\Activate.ps1
Your terminal prompt should now show (venv).

Install Dependencies


pip install -r requirements.txt
🧠 Prepare Model Files
Run dataset_creation.ipynb to generate dataset.csv.

Run model_training.ipynb to train the model and create:

ip_fraud_detection_model.pkl

label_encoders.pkl

Place these files in the model/ directory.

▶️ Run the Application
Navigate to the backend:


cd backend
Start the Flask server:

python app.py
Open your browser and visit:


http://localhost:5000
💻 Usage
🌍 Main Page
Enter an IP address (e.g., 8.8.8.8)

Click Check IP to view its fraud status

🛡️ Admin Panel
Visit: http://localhost:5000/admin/login

Login Credentials:

Username: admin

Password: password

After login, visit:


http://localhost:5000/admin/dashboard
Here you can:

View all IP check logs

Flag/unflag suspicious IPs

View prediction stats via pie charts (powered by Chart.js)

🧪 Model Details
Algorithm: RandomForestClassifier

Features Used:

IP Octets (numeric)

Country

ISP

Organization

Timezone

Encoding: Categorical features encoded via LabelEncoder

Training:

Hyperparameter tuning with GridSearchCV

Model saved as: ip_fraud_detection_model.pkl

Encoders saved as: label_encoders.pkl

Evaluation:

Accuracy and classification metrics

See model_training.ipynb for details

👥 Team Roles
👤 Team Member:

Created MVP

Built dataset_creation.ipynb, model_training.ipynb

Developed initial web app: app.py, index.html, script.js, style.css

👨‍💻 You:

Built Admin Panel: Login system, dashboard, flagging

Enhanced UI/UX: Input validation, error messages, better styling

Integrated Chart.js for data visualization

⚠️ Notes
🔒 Security: Login uses hardcoded credentials for simplicity.
Replace with a secure authentication system before production.

📦 Dependencies: All required packages are in requirements.txt

🗃️ Database: SQLite DB (ip_checks.db) is auto-created and .gitignored

❌ Excluded:

venv/ directory

Model files (*.pkl) must be generated locally