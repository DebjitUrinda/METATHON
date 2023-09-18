import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df1 = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/nlp_input.xlsx',sheet_name='nlp_input')#,header=None)

# Tokenize the text
nltk.download('punkt')
df1['Tokenized_Text'] = df1['User_Input'].apply(lambda x: nltk.word_tokenize(x))

# TF-IDF Vectorization on unlemmatized text
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df1['User_Input'])

# User input
user_input = input("Enter your query: ")#"dogs"

# Convert user input to lowercase
user_input = user_input.lower()

# Transform user input into TF-IDF vector on unlemmatized text
user_input_tfidf = tfidf_vectorizer.transform([user_input])

# Calculate cosine similarity between user input and DataFrame sentences
user_similarity_scores = cosine_similarity(user_input_tfidf, tfidf_matrix)

# Initialize an empty list to store confidence scores
confidence_scores = []

# Print similarity scores for clarity
print("Similarity Scores:")
for i, score in enumerate(user_similarity_scores[0]):
    print(f"User_Input {i + 1}: {score}")

# Set a similarity threshold (adjust this value as needed)
threshold = 0.1  # Adjust this threshold as per your requirement

# Calculate Confidence Scores based on the threshold
for i in range(len(user_similarity_scores[0])):
    if user_similarity_scores[0][i] >= threshold:
        confidence_scores.append(user_similarity_scores[0][i])
    else:
        confidence_scores.append(0.0)  # Confidence is 0 if below threshold

# Add the confidence scores to the DataFrame
df1['Confidence_Score'] = confidence_scores

# Display the DataFrame
print("\nDataFrame:")
# print(df)
# df1.droplevel(1)
max_index = df1['Confidence_Score'].idxmax()
print(df1.loc[max_index])