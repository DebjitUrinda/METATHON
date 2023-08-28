import pandas as pd
import random
import incident
import login
import ritm
import chg
import feedback

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
    print(argument)
    switcher = {
        RITM: RITM(),
        INC: INC(),
        CHG: CHG()
    }
    return switcher.get(argument, "nothing")

# function for RITM
def RITM():
    print(ritm.RITM())

# function for INC
def INC():
    # var = incident.Incident()
    print(incident.Incident()) 

# function for CHG
def CHG():
    print(chg.Change())


def main():
    x = login.Login()
    if (x == 1):
        print("ROBO: My name is Robo. I will help with your queries about VDI,account access etc.. If you want to exit, type Bye!")
        while(True):
            user_response = input("How may I help you: ")
            user_response=user_response.lower()
            
            if not user_response:  # Check for empty input
                print("ROBO: Please provide a valid input.")
                continue
            
            if(user_response!='bye'):
                if(user_response=='thanks' or user_response=='thank you' ):
                    flag=False
                    print("ROBO: You are welcome..")
                elif greeting(user_response) is not None:
                    print("ROBO: " + greeting(user_response))
                else:
                    print("ROBO: ", end="")
                    console_op = response(user_response)
                    console_list = console_op.split(":")
                    if len(console_list) > 1 and console_list[0].split(" ")[-2].upper() in ["RITM", "INC", "CHG"]:
                        print(console_list[0].split(" ")[-2].upper())
                        call_to_service_now(console_list[0].split(" ")[-2].upper())
                        print(console_op)
                        print(console_list)
                    else:
                        print("I'm sorry, but I didn't understand that. Could you please rephrase?")
                    sent_tokens.remove(user_response)
            else:
                flag=False
                print("ROBO: Bye! take care..")
                break

if __name__ == "__main__":
    main()
