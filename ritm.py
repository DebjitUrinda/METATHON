import requests
import pandas as pd

# ServiceNow API endpoint and credentials

def RITM(ritm_argument):
    ritm_df = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/RITM_INC_CHG-Details.xlsx',sheet_name='RITM_Sheet')
    ritm_df["User_Input"] = ritm_df["User_Input"].str.replace('.','',regex=False)
    ritm_df_unique = ritm_df.drop_duplicates(subset=['User_Input'])
    ritm_argument = ritm_argument.replace('.','')
    result_df = ritm_df_unique.loc[ritm_df_unique['User_Input'].str.lower()==ritm_argument]

    url = "https://dev78375.service-now.com/api/now/table/sc_req_item"
    username = "admin"
    password = "9%3fWxi^LiWW"
   
    # JSON payload for creating an Incident
    ritm_payload = {
    "short_description": str(result_df['User_Input'].iloc[0]),
    "description": str(result_df['Summary_of_Request'].iloc[0]),
    # "sys_created_by":"",
    # "contact_type": "",
    "context": str(result_df['Domain'].iloc[0]),
    "cat_item": str(result_df['Application_Name'].iloc[0]),
    # "request": "REQ0010001",
    }  
   
    # Set up authentication
    auth = (username, password)
   
    # Send POST request to create an Incident
    response = requests.post(url, json=ritm_payload, auth=auth)
    
    # Check response
    if response.status_code != 200:
        # print("RITM created successfully!")
        return(response.json().get('result').get('task_effective_number'))
    else:
        return(response.text)
    
# def main():
#     result=RITM("access request.")
#     print(result)

# if __name__ == "__main__":
#     main()