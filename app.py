from flask import Flask, request, jsonify
import csv
from datetime import datetime
from flask_cors import CORS
from bully_detector import classify_severity, save_log_local

app = Flask(__name__)
CORS(app)

LOG_FILE = "logs.csv"
REVIEWS_FILE = "reviews.csv"


# --- Home route ---
@app.route("/")
def home():
    return "✅ BullyBlock AI API is running! Use /stats, /analyze, /reports, or /reviews."


# --- Analyze a new message ---
@app.route("/analyze", methods=["POST"])
def analyze_message():
    data = request.json
    message = data.get("message", "")
    user_email = data.get("email", "anonymous")

    severity = classify_severity(message)
    save_log_local(user_email, message, severity)

    log_entry = {
        "user": user_email,
        "message": message,
        "severity": severity,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(log_entry)


# --- Get stats from logs ---
@app.route("/stats", methods=["GET"])
def get_stats():
    total = high = flagged = 0
    flagged_users = set()

    try:
        with open(LOG_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames or "Severity" not in reader.fieldnames:
                return jsonify({"total": 0, "high": 0, "flagged": 0})

            for row in reader:
                total += 1
                severity = row.get("Severity")
                user = row.get("User Email")

                if severity == "High":
                    high += 1
                    if user:
                        flagged_users.add(user)

        flagged = len(flagged_users)

    except FileNotFoundError:
        return jsonify({"total": 0, "high": 0, "flagged": 0})

    return jsonify({
        "total": total,
        "high": high,
        "flagged": flagged
    })


# --- Get full reports (for Reports page) ---
@app.route("/reports", methods=["GET"])
def get_reports():
    logs = []
    try:
        with open(LOG_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return jsonify([])

            for row in reader:
                logs.append({
                    "date": row.get("Timestamp", ""),
                    "user": row.get("User Email", "unknown"),
                    "message": row.get("Message", ""),
                    "severity": row.get("Severity", "")
                })

    except FileNotFoundError:
        return jsonify([])

    return jsonify(logs)


# --- Get full reviews (for Reviews page) ---
@app.route("/reviews", methods=["GET"])
def get_reviews():
    reviews = []
    try:
        with open(REVIEWS_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return jsonify([])

            for row in reader:
                reviews.append({
                    "timestamp": row.get("Timestamp", ""),
                    "bully_message": row.get("Bully Message", ""),
                    "review": row.get("Review", ""),
                    "sentiment": row.get("Sentiment", ""),
                    "sentiment_score": row.get("Sentiment Score", "")
                })

    except FileNotFoundError:
        return jsonify([])

    return jsonify(reviews)


if __name__ == "__main__":
    app.run(debug=True)
