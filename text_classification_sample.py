import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample labeled data
data = {
    'Text': [
        "vdi is working",
        "vdi not opening",
        # Add more labeled data here
    ],
    'Label': [
        "Factual",
        "Problem",
        # Add labels accordingly
    ]
}

df = pd.DataFrame(data)

# Feature extraction using CountVectorizer
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['Text'])

# Create and train the classifier
classifier = MultinomialNB()
classifier.fit(X, df['Label'])

# User input
user_input = input("Enter your message: ")

# Vectorize user input and predict its class
user_input_vector = vectorizer.transform([user_input])
predicted_label = classifier.predict(user_input_vector)

if predicted_label[0] == "Factual":
    print("User input is a factual statement.")
elif predicted_label[0] == "Problem":
    print("User input is a problem statement.")
else:
    print("User input could not be categorized.")
