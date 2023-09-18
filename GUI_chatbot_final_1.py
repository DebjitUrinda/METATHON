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
import incident_new as incident
import pandas as pd
import re
import ritm
import chg
import feedback
import text_classification_tuned as td
import os
import requests

warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('popular', quiet=True)  # for downloading packages

# uncomment the following only the first time
# nltk.download('punkt') # first-time use only
# nltk.download('wordnet') # first-time use only


# Reading in the corpus
with open('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/chatbot.txt', 'r', encoding='utf8',
          errors='ignore') as fin:
    raw = fin.read().lower()

# TOkenisation
sent_tokens = nltk.sent_tokenize(raw)  # converts to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
# def LemNormalize(text):
#     return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "hey")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Calling service_now through functions
def call_to_service_now(user_argument,argument,id):
    testing = user_argument
    func = argument
    if func == "RITM":
        return RITM(user_argument)
    elif func == "INC":
        return INC(user_argument,id)
    elif func == "CHG":
        return CHG(user_argument,id)

# function for RITM
def RITM(ritm_argument):
    robo_return = "ROBO: " + ritm.RITM(ritm_argument)
    return robo_return

# function for INC
def INC(inc_argument,id):
    # var = incident.Incident(inc_argument,str(id))
    robo_return = "ROBO: " + incident.Incident(inc_argument,str(id))
    return robo_return

# function for CHG
def CHG(chg_argument,id):
    robo_return = "ROBO: " + chg.Change(chg_argument,str(id))
    return robo_return


class LoginGUI:
    # ... (other methods and initialization)
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.username_label = tk.Label(root, text="Employee_ID:")
        self.username_label.pack(padx=10, pady=(20, 0))

        self.username_entry = tk.Entry(root, width=40)
        self.username_entry.pack(padx=10, pady=(0, 10))

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

    def login(self):
        try:
            already_data = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/login_details.xlsx')
        except FileNotFoundError:
            already_data = pd.DataFrame(columns=['Employee_ID', 'Full_Name','Phone_Number', 'E_mail'])

        ID_pattern = r'[0-9]{2,}'

        Employee_ID = int(self.username_entry.get())  # Get Employee_ID from input field
        global emp_id
        emp_id = Employee_ID

        if re.search(str(ID_pattern), str(Employee_ID)):
            filtered = already_data[already_data['Employee_ID'] == Employee_ID]

            if filtered.empty:
                # Ask if the user wants to register
                if messagebox.askyesno("Register", "Not an existing user. Do you want to register?"):
                    self.root.destroy()  # Close the login window
                    root = tk.Tk()
                    LoginGUI_newUser(root)
                    root.mainloop()  # Launch GUI for new users

            else:
                for index, row in filtered.iterrows():
                    messagebox.showinfo("Login Successful",
                                        f"Logged in as {row['Employee_ID']}.")
                    self.root.destroy()  # Close the login window
                    self.launch_chatbot_gui()
        else:
            messagebox.showerror("Invalid Employee ID", "Enter a valid Employee ID (at least 2 digits).")

    def launch_chatbot_gui(self):
        chatbot_root = tk.Tk()
        ChatbotGUI(chatbot_root)
        chatbot_root.mainloop()


class LoginGUI_newUser:
    def __init__(self, root):
        self.root = root
        self.root.title("New User Registration")

        self.employeeID_label = tk.Label(root, text="Employee_ID:")
        self.employeeID_label.pack(padx=10, pady=(20, 0))

        self.employeeID_entry = tk.Entry(root, width=40)
        self.employeeID_entry.pack(padx=10, pady=(0, 10))
       
        self.FullName_label = tk.Label(root, text="Full_Name:")
        self.FullName_label.pack(padx=10, pady=(20, 0))
       
        self.FullName_entry = tk.Entry(root, width=40)
        self.FullName_entry.pack(padx=10, pady=(0, 10))

        self.phone_label = tk.Label(root, text="Phone_Number:")
        self.phone_label.pack(padx=10, pady=(0, 0))

        self.phone_entry = tk.Entry(root, width=40)
        self.phone_entry.pack(padx=10, pady=(0, 20))

        self.email_label = tk.Label(root, text="Email:")
        self.email_label.pack(padx=10, pady=(0, 0))

        self.email_entry = tk.Entry(root, width=40)
        self.email_entry.pack(padx=10, pady=(0, 20))

        self.login_button = tk.Button(root, text="Continue to login", command=self.newLogin)
        self.login_button.pack()

    def newLogin(self):
        try:
            login_data = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/login_details.xlsx')
        except FileNotFoundError:
            login_data = pd.DataFrame(columns=['Employee_ID', 'Full_Name', 'Phone_Number', 'E_mail'])

        ID_pattern = r'[0-9]{2,}'
        name_pattern = r'^[A-Za-z]+( [A-Za-z]+)+$'
        phone_pattern = r'^\d{10}$'
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        Employee_ID = int(self.employeeID_entry.get())  # Get Employee_ID from input field

        if re.search(str(ID_pattern), str(Employee_ID)):
           
            Full_Name = self.FullName_entry.get()
            if re.search(str(name_pattern), str(Full_Name)):
               
                Phone_Number = self.phone_entry.get()  # Get Phone_number from input field
                if re.match(phone_pattern, Phone_Number):
                    E_mail = self.email_entry.get()  # Get E-mail from input field

                    if re.search(str(email_pattern), str(E_mail)):
                        new_login_data = pd.DataFrame({'Employee_ID': [Employee_ID],
                                                       'Full_Name': [Full_Name],
                                                       'Phone_Number': [Phone_Number],
                                                       'E_mail': [E_mail]})

                        login_data = pd.concat([login_data, new_login_data], ignore_index=True)
                        login_data.to_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/login_details.xlsx', index=False)

                        messagebox.showinfo("Registration Successful", "New Employee. Welcome!")
                        self.root.destroy()  # Close the login window
                        self.launch_chatbot_gui_new_user()
                    else:
                        messagebox.showerror("Invalid Employee", "Enter a valid numberic ID.")
                else:
                    messagebox.showerror("Invalid Name", "Enter Valid Full Name.")
            else:
                messagebox.showerror("Invalid Phone_Number", "Enter a valid 10 digit phone_number.")
        else:
            messagebox.showerror("Invalid E-Mail", "Enter a valid mail-id.")
               

               
           
    def launch_chatbot_gui_new_user(self):
        root = tk.Tk()
        LoginGUI(root)
        root.mainloop()

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
        self.append_response("You: "+user_message)
        if not user_response:  # Check for empty input
                self.append_response("ROBO: Please provide a valid input.")
                # continue
        elif user_response != "bye":
            if(user_response=='thanks' or user_response=='thank you' ):
                # flag=False
                self.append_response("ROBO: You are welcome..")
                self.root.destroy()
            elif greeting(user_response) is not None:
                self.append_response("ROBO: " + greeting(user_response))
            else:
                # print("ROBO: ", end="")
                flag = td.class_return(user_message)
                if flag:
                    robo_response = self.generate_response(user_response)
                    console_list = robo_response.split(":")
                    print(console_list)
                    if len(console_list) > 1 and console_list[0].upper() in ["RITM", "INC", "CHG"]:
                        self.append_response(console_list[0].upper())
                        robo_response = call_to_service_now(console_list[1],console_list[0].upper(),emp_id)
                        self.append_response(robo_response)
                        self.append_response("In")
                        # print(console_list)
                    else:
                        #take the feedback here into an error file
                        self.append_response("ROBO: "+feedback.feedback())
                else:
                    self.append_response("ROBO: "+"This is a fact")
                    return robo_response
                sent_tokens.remove(user_response)
        else:
            self.append_response("ROBO: Bye! take care.. :)"+"\n"+"Hope to serve you better next time!!")
            self.input_entry.config(state=tk.DISABLED)
            self.root.destroy()
           
        self.input_entry.delete(0, tk.END)
       
    def generate_response(self, user_message):
        robo_response = ''
        sent_tokens.append(user_message)
        TfidfVec = TfidfVectorizer(tokenizer=self.lem_normalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        user_input_tfidf = TfidfVec.transform([user_message])
        user_similarity_scores = cosine_similarity(user_input_tfidf,tfidf)
        # vals = cosine_similarity(tfidf[-1], tfidf)
        idx = user_similarity_scores.argsort()[0][-2]
        flat = user_similarity_scores.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            # robo_response = robo_response + "I am sorry! I don't understand you"
            self.append_response("ROBO: "+"I am sorry! I don't understand you"+"\n"+"Could you please rephrase")
            return robo_response
        else:
            # Set a similarity threshold (adjust this value as needed)
            threshold = 0.38  # Adjust this threshold as per your requirement

            # if user_similarity_scores[0][idx] >= threshold:
            for i in range(len(user_similarity_scores[0])):
                if user_similarity_scores[0][i] >= threshold:
                    robo_response = robo_response + sent_tokens[idx]
                    break
                # else:
                #     robo_response = robo_response + "I am not confident in my response."
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
    LoginGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()