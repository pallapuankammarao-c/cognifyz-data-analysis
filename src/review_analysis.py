"""
Review Text and Keyword Analysis Module for Cognifyz Restaurant Data.
Analyzes categorical rating text keywords, customer sentiment drivers, and provides
NLP text cleaning and n-gram keyword extraction.
"""

import re
from collections import Counter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Common English stopwords list for NLP tokenization
DEFAULT_STOPWORDS = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
    "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "restaurant",
    "food", "place", "service", "good", "great", "ordered"
])

POSITIVE_LEXICON = {
    "excellent", "delicious", "amazing", "fresh", "friendly", "superb", "loved", "best",
    "quick", "clean", "authentic", "pleasant", "tasty", "cozy", "perfection", "wonderful",
    "favorite", "outstanding", "hygienic", "courteous", "value"
}

NEGATIVE_LEXICON = {
    "horrible", "terrible", "slow", "cold", "bland", "worst", "rude", "dirty", "unhygienic",
    "stale", "overpriced", "disappointing", "bad", "average", "salty", "delay", "poor",
    "arrogant", "undercooked", "burnt", "noisy"
}


def clean_text(text: str) -> list[str]:
    """
    Cleans raw review text, strips punctuation/symbols, and removes stopwords.
    """
    if not isinstance(text, str):
        return []
    # Lowercase and strip non-alphabetic chars
    cleaned = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
    tokens = [w.strip() for w in cleaned.split() if len(w.strip()) > 2]
    return [w for w in tokens if w not in DEFAULT_STOPWORDS]


def extract_frequent_words(texts: list[str], top_n: int = 20) -> pd.DataFrame:
    """
    Extracts top frequent keywords and assigns lexicon polarity markers.
    """
    counter = Counter()
    for text in texts:
        tokens = clean_text(text)
        counter.update(tokens)

    data = []
    for word, count in counter.most_common(top_n):
        sentiment = "Neutral"
        if word in POSITIVE_LEXICON:
            sentiment = "Positive"
        elif word in NEGATIVE_LEXICON:
            sentiment = "Negative"
        data.append({"Keyword": word, "Frequency": count, "Sentiment_Hint": sentiment})

    return pd.DataFrame(data)


def analyze_rating_text_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes the 'Rating text' column distribution across aggregate ratings.
    """
    grouped = df.groupby(["Rating text", "Rating color"]).agg(
        Count=("Restaurant ID", "count"),
        Min_Rating=("Aggregate rating", "min"),
        Max_Rating=("Aggregate rating", "max"),
        Avg_Rating=("Aggregate rating", "mean"),
        Avg_Votes=("Votes", "mean"),
    ).reset_index()

    total = len(df)
    grouped["Percentage"] = (grouped["Count"] / total * 100).round(2)
    grouped["Avg_Rating"] = grouped["Avg_Rating"].round(2)
    grouped["Avg_Votes"] = grouped["Avg_Votes"].round(1)
    return grouped.sort_values(by="Avg_Rating", ascending=False)


def plot_rating_text_keywords_bar(freq_df: pd.DataFrame) -> go.Figure:
    """
    Plots horizontal bar chart of extracted text keywords.
    """
    sorted_df = freq_df.sort_values(by="Frequency", ascending=True)
    color_map = {"Positive": "#10b981", "Negative": "#ef4444", "Neutral": "#6366f1"}

    fig = px.bar(
        sorted_df,
        x="Frequency",
        y="Keyword",
        orientation="h",
        text="Frequency",
        color="Sentiment_Hint",
        title="Top Extracted Keywords (Lexicon Polarity Hint)",
        labels={"Frequency": "Occurrences", "Keyword": "Extracted Token"},
        color_discrete_map=color_map,
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def analyze_custom_review_text(text: str) -> dict:
    """
    Analyzes user-entered or uploaded review text samples.
    Note: Evaluates lexical frequency patterns without asserting full ML sentiment classification.
    """
    tokens = clean_text(text)
    total_tokens = len(tokens)
    if total_tokens == 0:
        return {
            "total_tokens": 0,
            "positive_count": 0,
            "negative_count": 0,
            "positive_keywords": [],
            "negative_keywords": [],
            "top_keywords": [],
        }

    pos_found = [w for w in tokens if w in POSITIVE_LEXICON]
    neg_found = [w for w in tokens if w in NEGATIVE_LEXICON]

    word_counts = Counter(tokens).most_common(10)

    return {
        "total_tokens": total_tokens,
        "positive_count": len(pos_found),
        "negative_count": len(neg_found),
        "positive_keywords": list(set(pos_found)),
        "negative_keywords": list(set(neg_found)),
        "top_keywords": word_counts,
    }
