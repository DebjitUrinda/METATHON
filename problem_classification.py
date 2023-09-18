import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV
import joblib
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

# specific_rows=['Factual']
data = {'Text':[]}
my_df = pd.DataFrame(data)
df = pd.read_csv('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/trained_fact_prob.csv',sep='|')
df = df[df['Label']=='Problem']
my_df['Text'] = df['Processed_Text']
print(my_df)

# # Data Preprocessing
# def preprocess(text):
#     ## Lowercasing
#     text = text.lower()
#     ## Remove punctuation
#     text = text.translate(str.maketrans('', '', string.punctuation))

#     ## Tokenize the text
#     tokens = nltk.word_tokenize(text)
#     ## StopWord Removal
#     stop_words = set(stopwords.words('english'))
#     text = [word for word in tokens if word.lower() not in stop_words]
#     # Lemmatize the tokens
#     lemmatizer = WordNetLemmatizer()
#     tokens = [lemmatizer.lemmatize(token) for token in tokens]
#     ## Removing special characters and numbers
#     text = [word for word in tokens if word.isalpha()]

#     # Joining the tokens back to a single string after pre-processing
#     return " ".join(tokens)

# # Dataset pre-processing
# df['Processed_Text'] = df['Text'].apply(preprocess)

# # Splitting the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(df['Processed_Text'], df['Label'], test_size=0.0000000000001, random_state=42)

# # Feature Extraction using TF-IDF Vectorization
# vectorizer = TfidfVectorizer()
# X_train_tfidf = vectorizer.fit_transform(X_train)
# # X_test_tfidf = vectorizer.transform(X_test)

# # Model Selection (Random Forest Classifier)
# rf_classifier = RandomForestClassifier()

# # Hyperparameter Tuning using Grid Search
# param_grid = {
#     'n_estimators': [100, 200, 300],
#     'max_depth': [None, 10, 20, 30],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }

# grid_search = GridSearchCV(estimator=rf_classifier, param_grid=param_grid, cv=2, n_jobs=-1)
# grid_search.fit(X_train_tfidf, y_train)

# # Best hyperparameters
# best_params = grid_search.best_params_

# # Model Training with Best Hyperparameters
# best_rf_classifier = RandomForestClassifier(**best_params)
# best_rf_classifier.fit(X_train_tfidf, y_train)

# # Saving the trained model to a file
# model_filename = '/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/rf_classifier_model.pkl'
# joblib.dump(best_rf_classifier, model_filename)

# # # Model Evaluation
# # y_pred = best_rf_classifier.predict(X_test_tfidf)
# # accuracy = accuracy_score(y_test, y_pred)
# # report = classification_report(y_test, y_pred)

# # print("Accuracy:", accuracy)
# # print("Classification Report:\n", report)

# # Load the trained model from the file
# loaded_model = joblib.load('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/rf_classifier_model.pkl')

# # User Input
# user_input = input("Enter your query: ")

# # Preprocess User Input
# user_input_processed = preprocess(user_input)
# user_input_tfidf = vectorizer.transform([user_input_processed])

# # Make Predictions
# user_prediction = loaded_model.predict(user_input_tfidf)


# # Display Results
# if user_prediction[0] == "Factual":
#     result = {'Text': [user_input], 'Label':['Factual']}
#     df1 = pd.DataFrame(result)
#     df1['Processed_Text'] = df1['Text'].apply(preprocess)
#     df = df.append(df1, ignore_index=True)
#     print("Model Prediction: This is a factual statement.")
# elif user_prediction[0] == "Problem":
#     result = {'Text': [user_input], 'Label':['Problem']}
#     df1 = pd.DataFrame(result)
#     df1['Processed_Text'] = df1['Text'].apply(preprocess)
#     df = df.append(df1, ignore_index=True)
#     print("Model Prediction: This indicates a problem.")
# else:
#     print("Model Prediction: Unable to classify.")

# df.to_csv('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/trained_fact_prob.csv',sep='|',index=False)
# print(df.tail())