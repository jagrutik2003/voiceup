# VoiceUp Analytics & Compliance: Backend and Database
This document outlines the setup, configuration, and testing of the backend and database for the VoiceUp Analytics & Compliance project. The backend is built with Flask, uses a PostgreSQL database (voiceup_db), and integrates a Transformers-based emotion detection model.

# Project Structure

src/app.py: Flask application with API endpoints.
src/analysis.py: Emotion analysis logic using Transformers.
src/models.py: SQLAlchemy models for database tables.
src/download_model.py: Script to download the emotion model.
models/emotion-model/: Directory for the pre-trained emotion model.

# Prerequisites

Python 3.8+: Install from https://www.python.org/downloads/.
PostgreSQL 13+: Install from https://www.postgresql.org/download/windows/.
PowerShell: For running commands on Windows.
Project Directory: C:\Users\hp\Desktop\voice-analytics.

# Setup Instructions
1. Navigate to Project Directory
cd C:\Users\hp\Desktop\voice-analytics

2. Create and Activate Virtual Environment
python -m venv venv
.\venv\Scripts\activate


3. Set Up PostgreSQL Database

Create Database:
createdb -U postgres voiceup_db

Enter the password : aaJJ10@@

Initialize Tables:Ensure src/models.py defines conversations, messages, and analysis_results tables:
python -c "from src.app import app, db; app.app_context().push(); db.create_all()"


Verify Schema:
psql -U postgres -d voiceup_db -c "\dt"

Expected output:
Schema |       Name        | Type  |  Owner
--------+-------------------+-------+---------
public | analysis_results  | table | postgres
public | conversations     | table | postgres
public | messages          | table | postgres


Verify Data:
psql -U postgres -d voiceup_db -c "SELECT * FROM messages;"

Expected: 4 rows with conversation_id=2,3.


4. Run Flask Server
flask --app src/app run --debug --host=127.0.0.1 --port=5000

Expected output:
 * Serving Flask app 'src/app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000

Testing Endpoints
Use PowerShell’s Invoke-WebRequest (as curl is an alias for it):

Basic Endpoint:
Invoke-WebRequest -Uri http://127.0.0.1:5000/ | Select-Object -ExpandProperty Content

Expected:
{"message":"Welcome to the VoiceUp Analytics API!"}


Per-Message Emotion Analysis:
Invoke-WebRequest -Method POST -Uri http://127.0.0.1:5000/api/messages/1/analyze | Select-Object -ExpandProperty Content

Expected:
{"emotions":[{"label":"positive","score":0.999},...]}


Conversation Analysis:
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/conversations/2/analysis | Select-Object -ExpandProperty Content

Expected:
{
  "emotion_summary": {"emotions": [{"label": "positive", "score": 0.8}, ...]},
  "compliance_summary": {"greeting": true, ...},
  "overall_compliance_score": 80,
  "analyzed_at": "..."
}


Conversations List:
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/conversations | Select-Object -ExpandProperty Content


Compliance Analytics:
Invoke-WebRequest -Uri http://127.0.0.1:5000/api/analytics/compliance | Select-Object -ExpandProperty Content






