import pandas as pd
import random
import incident
import string
import warnings
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

warnings.filterwarnings('ignore')
nltk.download('popular', quiet=True)
lemmer = WordNetLemmatizer()

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        self.username_label = tk.Label(root, text="Username:")
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
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Implement your actual login logic here
        # For example, you can compare the username and password with stored values
        if username == "your_username" and password == "your_password":
            self.root.destroy()  # Close the login window
            self.launch_chatbot_gui()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def launch_chatbot_gui(self):
        chatbot_root = tk.Tk()
        chatbot_gui = ChatbotGUI(chatbot_root)
        chatbot_root.mainloop()

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot GUI")
        
        self.text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=50)
        self.text_widget.pack(padx=10, pady=10)
        
        self.input_label = tk.Label(root, text="You:")
        self.input_label.pack(padx=10, pady=(0, 5))
        
        self.input_entry = tk.Entry(root, width=40)
        self.input_entry.pack(padx=10, pady=(0, 10))
        
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack()
        
        self.response_label = tk.Label(root, text="ROBO:")
        self.response_label.pack(padx=10, pady=(10, 5))
        
        self.response_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=50, state=tk.DISABLED)
        self.response_widget.pack(padx=10, pady=10)

    def send_message(self):
        user_message = self.input_entry.get()
        if user_message.lower() == "bye":
            self.append_response("ROBO: Bye! take care..")
            self.input_entry.config(state=tk.DISABLED)
        else:
            robo_response = self.generate_response(user_message)
            self.append_response("ROBO: " + robo_response)
            
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
            robo_response = robo_response + "I am sorry! I don't understand you"
            print("Please call the toll-free number of CTS")
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
        return LemTokens(nltk.word_tokenize(text.lower().translate(self.remove_punct_dict)))

def main():
    root = tk.Tk()
    login_gui = LoginGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
