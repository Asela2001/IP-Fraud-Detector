IP Fraud Detection System

Project Overview

This project implements a web-based IP Fraud Detection System designed to identify potentially fraudulent IP addresses using machine learning. The system includes a Minimum Viable Product (MVP) with a trained RandomForestClassifier model, a Flask web application, and an admin panel for monitoring and managing IP checks. The application fetches IP details from the ip-api.com API, predicts fraud status, and allows admins to flag suspicious IPs.
Setup Instructions
Prerequisites

Python 3.8+
Git

Installation

Clone the Repository:
git clone https://github.com/your-username/ip-fraud-detector.git
cd ip-fraud-detector


Create a Virtual Environment:
python -m venv venv


Activate it (Windows PowerShell):.\venv\Scripts\Activate.ps1


Your terminal prompt should show (venv).


Install Dependencies:

Install required packages from requirements.txt:pip install -r requirements.txt




Prepare Model Files:

Run model_training.ipynb with dataset.csv (from dataset_creation.ipynb) to generate ip_fraud_detection_model.pkl and label_encoders.pkl.
Place these files in the model/ folder.


Run the Application:

Start the Flask app:
cd \backend
python app.py


Access the app at http://localhost:5000.



Usage

Main Page: Enter an IP address (e.g., 8.8.8.8) to check its fraud status.
Admin Panel:
Go to http://localhost:5000/admin/login.
Log in with username admin and password password.
View the dashboard at http://localhost:5000/admin/dashboard to see IP checks, flag IPs, and view a pie chart of predictions.



Model Explanation

Model: A RandomForestClassifier trained on a dataset of IP addresses labeled as safe (0) or suspicious (1).
Features: Includes IP octets (numerical), country, ISP, organization, and timezone (encoded using LabelEncoder).
Training: Performed with hyperparameter tuning via GridSearchCV, saved as ip_fraud_detection_model.pkl. Label encoders are saved as label_encoders.pkl.
Performance: Evaluated with accuracy and classification metrics (details in model_training.ipynb).

Team Roles

Team Member: Developed the initial MVP, including dataset creation (dataset_creation.ipynb), model training (model_training.ipynb), and basic web app (app.py, index.html, script.js, style.css).
You: Enhanced the web application with an admin panel (login system, dashboard, flagging functionality, Chart.js visualization) and improved the user interface (input validation, error messages, styling).

Notes

Security: The admin login uses hardcoded credentials (admin/password) for simplicity. For production, replace with a secure authentication system.
Dependencies: Ensure all required packages are installed as listed in requirements.txt.
Database: The SQLite database (ip_checks.db) is created automatically and excluded from version control.
Excluded Files: The venv/ folder and model files are not included in the repository; users must generate them locally.
Last Updated: August 06, 2025, 10:05 PM +0530.
