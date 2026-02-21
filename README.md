# BullyBlock AI

## Project Overview
BullyBlock AI is a real-time AI-based system that detects and analyzes cyberbullying and cyberhate content using advanced Natural Language Processing (NLP) techniques.  
It aligns with UN SDG 16 – Peace, Justice, and Strong Institutions.

---

## Steps to Execute the Project

### Prerequisites
- Python 3.x installed
- VS Code IDE
- Internet connection

### Setup Instructions
1. Clone or download this repository to your local system.
2. Open the project folder in **VS Code**.
3. Install the required dependencies by running:
4. **Run the backend script and AI detection module**
```bash
python app.js
python bully_detector.py
6. Enter any sample message when prompted in the terminal.  
Example: `You are a shit`
7. The system will:
- Analyze the message using the **BERT** model.
- Ask for user feedback (good/bad).
- Categorize the message as **Low**, **Medium**, or **High** severity.
- Store low-severity data in the database.
- Send email alerts for high-severity cases with message details and timestamp.

---

## Dashboard Access
1. Open the registration page and create a new account.
2. Log in with your credentials.
3. After successful login, access the **dashboard**, which displays:
- Number of **Low**, **Medium**, and **High** severity messages.
- Sentiment analysis graphs.
- Model accuracy and performance metrics.
- Reports of detected messages.

---

## Output
- Real-time detection and severity classification of bullying messages.  
- Automatic email alerts for high-severity cases.  
- Interactive dashboard for report viewing and performance visualization.  
- Model Accuracy: **88% using BERT**

---
