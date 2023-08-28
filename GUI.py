import random
import string
import warnings
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import incident
import login
import ritm
import chg
import feedback
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
# def LemNormalize(text):
#     return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Calling service_now through functions
def call_to_service_now(argument):
    func = argument
    if func == "RITM":
        return RITM()
    elif func == "INC":
        return INC()  
    elif func == "CHG":
        return CHG()
    else:
        return "Sorry, I can only help you with INC/RITM/CHG as of now."+"\n"+"Our Team is working hard to incorporate more options. Thank you!!!"    # Call the selected function

# function for RITM
def RITM():
    robo_return = "ROBO: " + ritm.RITM()
    return robo_return

# function for INC
def INC():
    # var = incident.Incident()
    robo_return = "ROBO: " + incident.Incident()
    return robo_return 

# function for CHG
def CHG():
    robo_return = "ROBO: " + chg.Change()
    return robo_return

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        self.username_label = tk.Label(root, text="User_ID:")
        self.username_label.pack(padx=10, pady=(20, 0))
        
        self.username_entry = tk.Entry(root, width=40)
        self.username_entry.pack(padx=10, pady=(0, 10))
        
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack(padx=10, pady=(0, 0))
        
        self.password_entry = tk.Entry(root, show="*", width=40)
        self.password_entry.pack(padx=10, pady=(0, 20))
        
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        user_id = self.username_entry.get()
        password = self.password_entry.get()
        
        x=login.Login(user_id,password)
        if (x==1):
            self.root.destroy()  # Close the login window
            self.launch_chatbot_gui()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def launch_chatbot_gui(self):
        chatbot_root = tk.Tk()
        # global chatbot_gui
        # chatbot_gui = 
        ChatbotGUI(chatbot_root)
        chatbot_root.mainloop()

class ChatbotGUI:
    def __init__(self):
        pass
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot GUI")
        
        self.input_label = tk.Label(root, text="How may I help you?")
        self.input_label.pack(padx=10, pady=(10, 0))
        
        self.input_entry = tk.Entry(root, width=40)
        self.input_entry.pack(padx=10, pady=(0, 10))
        
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()
        
        self.response_label = tk.Label(root, text="ROBO:")
        self.response_label.pack(padx=10, pady=(10, 0))
        
        self.response_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=50, state=tk.DISABLED)
        self.response_widget.pack(padx=10, pady=(0, 10))


    def send_message(self):
        user_message = self.input_entry.get()
        user_response=user_message.lower()
        if not user_response:  # Check for empty input
                self.append_response("ROBO: Please provide a valid input.")
                # continue
        elif user_response != "bye":
            if(user_response=='thanks' or user_response=='thank you' ):
                # flag=False
                self.append_response("ROBO: You are welcome..")
            elif greeting(user_response) is not None:
                self.append_response("ROBO: " + greeting(user_response))
            else:
                # print("ROBO: ", end="")
                robo_response = self.generate_response(user_response)
                console_list = robo_response.split(":")
                if len(console_list) > 1 and console_list[0].split(" ")[-2].upper() in ["RITM", "INC", "CHG"]:
                    self.append_response(console_list[0].split(" ")[-2].upper())
                    robo_response = call_to_service_now(console_list[0].split(" ")[-2].upper())
                    self.append_response(robo_response)
                    # print(console_list)
                else:
                    #take the feedback here into an error file
                    self.append_response("ROBO: "+feedback.feedback())
                sent_tokens.remove(user_response)
        else:
            self.append_response("ROBO: Bye! take care.. :)"+"\n"+"Hope to serve you better next time!!")
            self.input_entry.config(state=tk.DISABLED)
            
        self.input_entry.delete(0, tk.END)
        
    def generate_response(self, user_message):
        robo_response = ''
        sent_tokens.append(user_message)
        TfidfVec = TfidfVectorizer(tokenizer=self.lem_normalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            # robo_response = robo_response + "I am sorry! I don't understand you"
            self.append_response("ROBO: "+"I am sorry! I don't understand you"+"\n"+"Could you please rephrase")
            return robo_response
        else:
            robo_response = robo_response + sent_tokens[idx]
            return robo_response

    def append_response(self, response):
        self.response_widget.config(state=tk.NORMAL)
        self.response_widget.insert(tk.END, response + "\n")
        self.response_widget.config(state=tk.DISABLED)
        self.response_widget.see(tk.END)

    def lem_normalize(self, text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def main():
    root = tk.Tk()
    # login_gui = 
    LoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
