# train_model.py
from pathlib import Path
import pandas as pd
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import matplotlib.pyplot as plt
import seaborn as sns

from xgboost import XGBClassifier

# ---------------------------
# 🔹 Setup
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA = BASE_DIR / "cyberbullying_tweets.csv"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

# ---------------------------
# 🔹 Load dataset
# ---------------------------
df = pd.read_csv(DATA)
df = df[['tweet_text', 'cyberbullying_type']].dropna()

# Label: 1 = bullying, 0 = safe
df['label'] = df['cyberbullying_type'].apply(lambda x: 0 if x == 'not_cyberbullying' else 1)

# ---------------------------
# 🔹 Preprocessing: stopwords + stemming
# ---------------------------
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def clean(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", " ", str(text).lower()).strip()
    words = [stemmer.stem(w) for w in text.split() if w not in stop_words]
    return " ".join(words)

df['tweet_text'] = df['tweet_text'].apply(clean)

# ---------------------------
# 🔹 Train-test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    df['tweet_text'], df['label'], test_size=0.2, stratify=df['label'], random_state=42
)

# ---------------------------
# 🔹 TF-IDF vectorization (1-4 ngrams, more features)
# ---------------------------
vectorizer = TfidfVectorizer(min_df=2, ngram_range=(1, 4), max_features=150000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ---------------------------
# 🔹 Train XGBoost model (tuned)
# ---------------------------
model = XGBClassifier(
    n_estimators=500,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='logloss',
    n_jobs=-1
)
model.fit(X_train_vec, y_train)

# ---------------------------
# 🔹 Evaluate
# ---------------------------
pred = model.predict(X_test_vec)
acc = accuracy_score(y_test, pred)
print(f"✅ Trained. Test accuracy: {acc:.3f}", flush=True)

# Save model and vectorizer
joblib.dump(model, MODELS_DIR / "bully_model_xgb.pkl")
joblib.dump(vectorizer, MODELS_DIR / "vectorizer.pkl")
print("✅ Saved to models/bully_model_xgb.pkl and models/vectorizer.pkl", flush=True)

# ---------------------------
# 🔹 Metrics + Graphs
# ---------------------------
# Confusion matrix
cm = confusion_matrix(y_test, pred)
plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig(IMAGES_DIR / "confusion_matrix.png", dpi=300)
plt.close()

# Accuracy bar graph
plt.bar(["Accuracy"], [acc])
plt.ylim(0, 1)
plt.title(f"Overall Accuracy = {acc:.2f}")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig(IMAGES_DIR / "accuracy.png", dpi=300)
plt.close()

# Classification report
report = classification_report(y_test, pred, output_dict=True)
print("\nClassification Report:")
print(classification_report(y_test, pred), flush=True)

# Per-class F1-score graph
classes = [str(c) for c in report.keys() if c not in ("accuracy", "macro avg", "weighted avg")]
f1_scores = [report[c]["f1-score"] for c in classes]

plt.figure(figsize=(6, 4))
sns.barplot(x=classes, y=f1_scores, palette="viridis")
plt.ylim(0, 1)
plt.title("Per-class F1 Scores")
plt.xlabel("Class")
plt.ylabel("F1 Score")
plt.tight_layout()
plt.savefig(IMAGES_DIR / "f1_scores.png", dpi=300)
plt.close()

print("📊 Figures saved to 'images/' folder: accuracy.png, confusion_matrix.png, f1_scores.png", flush=True)
