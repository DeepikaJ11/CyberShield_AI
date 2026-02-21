# bully_detector.py (updated with bully + review logging)
import os
import torch
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import csv

# import sentiment classifier you created
from review_detector import classify_sentiment

# === Email Config ===
EMAIL_SENDER = "bullyblockai@gmail.com"
EMAIL_RECEIVER = "bullyblockai@gmail.com"
EMAIL_APP_PASSWORD = os.environ.get("EMAIL_APP_PASSWORD", "slbmuxkzhnsapjgy")

# === Rule-based toxic keywords (extra safety) ===
TOXIC_WORDS = ["stupid", "idiot", "ugly", "hate", "kill", "moron", "loser", "foolish", "dumb"]

# === Load Toxic-BERT model ===
print("⏳ Loading Toxic-BERT model...")
tokenizer = AutoTokenizer.from_pretrained("unitary/toxic-bert")
bert_model = AutoModelForSequenceClassification.from_pretrained("unitary/toxic-bert")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_model.to(device)
print("✅ Loaded Toxic-BERT model successfully")

def classify_severity(text):
    """Classify message severity using rules + Toxic-BERT with probability thresholds"""
    for word in TOXIC_WORDS:
        if word in text.lower():
            return "High", 1.0  # forced high

    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = bert_model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]  # [non-toxic, toxic]

    toxic_score = probs[1].item()

    if toxic_score < 0.3:
        return "Low", toxic_score
    elif 0.3 <= toxic_score < 0.7:
        return "Medium", toxic_score
    else:
        return "High", toxic_score

def send_email(subject, body):
    """Send email alert"""
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_APP_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("📧 Email sent successfully!")
    except Exception as e:
        print(f"❌ Email failed: {e}")

def save_log_local(user_email, message, severity, toxic_score):
    """Save toxicity logs to logs.csv"""
    with open("logs.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Timestamp", "User Email", "Message", "Severity", "Toxic Score"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_email,
            message,
            severity,
            round(toxic_score, 3)
        ])
    print("📝 Saved locally to logs.csv")

def save_review_local(bully_message, review_text, sentiment_label, sentiment_score):
    """Save bully message + review + sentiment to reviews.csv"""
    with open("reviews.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Timestamp", "Bully Message", "Review", "Sentiment", "Sentiment Score"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            bully_message,
            review_text,
            sentiment_label,
            round(sentiment_score, 3)
        ])
    print("📝 Saved review to reviews.csv")

def main():
    user_email = EMAIL_SENDER
    user_input = input("Message: ").strip()
    if not user_input:
        print("No message entered. Exiting.")
        return

    severity, toxic_score = classify_severity(user_input)

    if severity == "Low":
        print(f"✅ SAFE: Message allowed. (Score: {toxic_score:.2f})")
    elif severity == "Medium":
        print(f"⚠️ MEDIUM: Message deleted. (Score: {toxic_score:.2f})")
    elif severity == "High":
        print(f"🚨 HIGH: Message deleted & email alert sent. (Score: {toxic_score:.2f})")
        subject = "🚨 BullyBlock AI Alert – High Toxicity Detected"
        body = (
            f"A high toxicity message was detected.\n\n"
            f"User: {user_email}\n"
            f"Message: {user_input}\n"
            f"Severity: {severity}\n"
            f"Toxic Score: {toxic_score:.2f}\n"
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        send_email(subject, body)

    save_log_local(user_email, user_input, severity, toxic_score)

    # --- NEW: Ask for review and classify sentiment ---
    review_input = input("Review (type something and press Enter): ").strip()
    if review_input:
        sentiment_label, sentiment_score = classify_sentiment(review_input)
        print(f"🔍 Review Sentiment: {sentiment_label} (score: {sentiment_score:.2f})")
        save_review_local(user_input, review_input, sentiment_label, sentiment_score)
    else:
        print("No review entered. Done.")

if __name__ == "__main__":
    main()
