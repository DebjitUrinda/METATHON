import pandas as pd

def Login(user_id,password):
    try:
        login_data = pd.read_excel('C:/Users/Siddhartha Sen/PycharmProjects/pythonProject/login_details.xlsx')

    except FileNotFoundError:
        login_data = pd.DataFrame(columns=['User_ID', 'Password'])

    # DataFrame for login deatils
    new_login_data = pd.DataFrame({'User_ID': [user_id], 'Password': [password]})
    login_data = pd.concat([login_data, new_login_data], ignore_index=True)
    # Save the DataFrame to an Excel file
    login_data.to_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/login_details.xlsx', index=False)
    # print("Login successful!")
    return 1