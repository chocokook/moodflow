from textblob import TextBlob

def analyze_sentiment(text: str) -> float:
    """Return polarity score between -1 (negative) to 1 (positive)."""
    return round(TextBlob(text).sentiment.polarity, 3)

def map_score_to_emoji(score: float) -> str:
    if score > 0.5:
        return "😄"
    elif score > 0.1:
        return "🙂"
    elif score > -0.1:
        return "😐"
    elif score > -0.5:
        return "😢"
    else:
        return "😡"
