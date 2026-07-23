from .moderator import analyze_toxicity
from .sentiment import analyze_sentiment
from .summarizer import summarize_text


def analyze_combo(text):
    result = {
        "sentiment": analyze_sentiment(text),
        "toxicity": analyze_toxicity(text),
    }

    if len(text) >= 100:
        result["summary"] = summarize_text(text)
    else:
        result["summary"] = None

    return result