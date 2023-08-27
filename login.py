import pandas as pd

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