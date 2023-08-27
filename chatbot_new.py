import pandas as pd
import random
import incident

import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


#Reading in the corpus
with open('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        # print(type(robo_response))
        return robo_response
    

# Calling service_now through functions
def call_to_service_now(argument):
    switcher = {
        RITM: RITM(),
        INC: INC(),
        CHG: CHG(),
    }
    return switcher.get(argument, "nothing")

# function for RITM
def RITM():
    return "RITM yet to be done"

# function for INC
def INC():
    # var = incident.Incident()
    print(incident.Incident()) 

# function for CHG
def CHG():
    return "CHG yet to be done"


def Login():
    try:
        login_data = pd.read_excel('C:/Users/Siddhartha Sen/PycharmProjects/pythonProject/login_details.xlsx')

    except FileNotFoundError:
        login_data = pd.DataFrame(columns=['Employee_ID', 'Username', 'Password'])

    # input for login
    ID = input("Enter your Employee_ID: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    # DataFrame for login deatils
    new_login_data = pd.DataFrame({'Employee_ID': [ID], 'Username': [username], 'Password': [password]})
    login_data = pd.concat([login_data, new_login_data], ignore_index=True)
    # Save the DataFrame to an Excel file
    login_data.to_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/login_details.xlsx', index=False)
    print("Login successful!")
    return 1

def main():
    x = Login()
    if (x == 1):
        print("ROBO: My name is Robo. I will answer your queries about Chatbots. If you want to exit, type Bye!")
        while(True):
            user_response = input("You: ")
            user_response=user_response.lower()
            if(user_response!='bye'):
                if(user_response=='thanks' or user_response=='thank you' ):
                    flag=False
                    print("ROBO: You are welcome..")
                else:
                    if(greeting(user_response)!=None):
                        print("ROBO: "+greeting(user_response))
                    else:
                        print("ROBO: ",end="")
                        console_op = response(user_response)
                        console_list = console_op.split(":")
                        # print(console_list)
                        call_to_service_now(console_list[0].split(" ")[-1].upper)
                        print(console_op)                        
                        # print(type(response))
                        sent_tokens.remove(user_response)
            else:
                flag=False
                print("ROBO: Bye! take care..")
                break

if __name__ == "__main__":
    main()
