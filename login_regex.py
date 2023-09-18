import pandas as pd

import re

 

def newLogin():

    try:

        login_data = pd.read_excel('C:/Users/888468/Downloads/today/login_details.xlsx')

    except FileNotFoundError:

        login_data = pd.DataFrame(columns=['Employee_ID','Employee_username','Mobile_number'])

   

    #input for login

    username_pattern = r'[a-zA-Z0-9]{2,}'

    ID_pattern = r'[0-9]{2,}'

    mobile_pattern = r'^\d{10}$'

    Employee_ID = int(input("Enter your Employee_ID: "))

   

    if re.search(str(ID_pattern) , str(Employee_ID)):

        print("ID pattern matching")

        Employee_username = input("Enter your username: ")

        if re.match(username_pattern , Employee_username):

            print("username pattern matching")

            Mobile_number = int(input("Enter your phone_number: "))

            if re.search(str(mobile_pattern) , str(Mobile_number)):

                print("mobile pattern matching")

               

                # DataFrame for login deatils

                new_login_data = pd.DataFrame({'Employee_ID': [Employee_ID],'Employee_username': [Employee_username],'Mobile_number': [Mobile_number]})

               

                login_data = pd.concat([login_data,new_login_data],ignore_index=True)

                # Save the DataFrame to an Excel file

                login_data.to_excel('C:/Users/888468/Downloads/today/login_details.xlsx', index=False)

               

                print("New Employee. Welcome!")

                return 0

               

            else:

                print("Enter mobile number correctly")   

        else:

            print("Enter username details correctly")

    else:

        print("Enter ID details correctly")

   

def Login():

    try:

        already_data = pd.read_excel('C:/Users/888468/Downloads/today/login_details.xlsx')

    except FileNotFoundError:

        already_data = pd.DataFrame(columns=['Employee_ID','Employee_username','Mobile_number'])

   

    ID_pattern = r'[0-9]{2,}'

    username_pattern = r'[a-zA-Z0-9]{2,}'

   

    Employee_ID = int(input("Enter your ID: "))

   

    if re.search(str(ID_pattern) , str(Employee_ID)):

        print("ID pattern matching")

        filtered = already_data[already_data['Employee_ID'] == Employee_ID]

       

        if filtered.empty:

            return 1

           

        else:

            for index, row in filtered.iterrows():

                print("ID :", row["Employee_ID"])

                print("username :", row["Employee_username"])

                mobile_number = row["Mobile_number"]

                print("Mobile_number:",int(mobile_number))

                return 0

    else:

        print("Enter ID details correctly")

   

def main():

    x = Login()

   

    if x == 0:

        print("Logged in")

    if x == 1:

        print("Not an user.If you want to register enter yes/no")

        if(input().lower() == 'yes'):

            newLogin()

        else:

            print("Good Bye")

       

    

if __name__ == "__main__":

    main()