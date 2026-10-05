from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client

from email.mime.text import MIMEText
import base64
import os

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


# Gmail API scope
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


# Load environment variables from .env
load_dotenv()


# Create Flask application
app = Flask(__name__)


# Allow frontend to communicate with backend
CORS(app)


# Get Supabase details from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# Create Supabase client
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# Create Gmail service
def get_gmail_service():
    credentials = Credentials(
        token=None,
        refresh_token=os.getenv("GOOGLE_REFRESH_TOKEN"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scopes=GMAIL_SCOPES,
    )

    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


# Home route
@app.route("/")
def home():
    return "Task Manager Backend is Running!"


# Test Supabase connection
@app.route("/test-db")
def test_db():
    response = supabase.table("users").select("*").execute()

    return {
        "message": "Supabase connection successful",
        "users": response.data
    }


# Send email using Gmail API
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.json

    to_email = data.get("to_email")
    subject = data.get("subject")
    body = data.get("body")

    if not to_email or not subject or not body:
        return {
            "message": "to_email, subject and body are required"
        }, 400

    message = MIMEText(body)

    message["to"] = to_email
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service = get_gmail_service()

    result = service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    return {
        "message": "Email sent successfully",
        "id": result.get("id")
    }


# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)