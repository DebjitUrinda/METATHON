import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()
user_input = input("Enter your message: ")

# Analyze sentiment
sentiment_scores = sia.polarity_scores(user_input)

# Determine sentiment based on the compound score
compound_score = sentiment_scores['compound']

if compound_score >= 0.0:
    print("User input is positive.")
elif compound_score <=-0.2:
    print("User input is negative.")
else:
    print("User input is neutral.")
