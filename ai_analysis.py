from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_bio_sentiment(bio):
    sia = SentimentIntensityAnalyzer()
    score = sia.polarity_scores(bio)
    if score['compound'] >= 0.05:
        return "Positif"
    elif score['compound'] <= -0.05:
        return "Negatif"
    else:
        return "Netral"
