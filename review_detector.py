# review_detector.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# device (use GPU if available)
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Lazy-loaded tokenizer + model so importing this file is cheap until you call classify_sentiment()
_tokenizer = None
_model = None

def _load_sentiment_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        # DistilBERT fine-tuned on SST-2 — simple positive/negative
        _tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        _model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        _model.to(_device)

def classify_sentiment(text):
    """
    Returns (label, positive_probability)
    label is "Positive" or "Negative"
    """
    _load_sentiment_model()
    inputs = _tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128).to(_device)
    with torch.no_grad():
        outputs = _model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]  # [neg, pos]
    positive_prob = probs[1].item()
    label = "Positive" if positive_prob >= 0.5 else "Negative"
    return label, positive_prob
