from textblob import TextBlob

user_input = input("Enter your message: ")
analysis = TextBlob(user_input)
sentiment = analysis.sentiment.polarity
if sentiment > 0:
    print("User input is positive.")
elif sentiment < 0:
    print("User input is negative.")
else:
    print("User input is neutral.")