import requests
import pandas as pd

# ServiceNow API endpoint and credentials
def Incident(inc_argument,emp_id):
    inc_df = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/RITM_INC_CHG-Details.xlsx',sheet_name='INC_Sheet')
    inc_df["Short_Description"] = inc_df["Short_Description"].str.replace('.','',regex=False)
    inc_df_unique = inc_df.drop_duplicates(subset=['Short_Description'])
    result_df = inc_df_unique.loc[inc_df_unique['Short_Description']==inc_argument]

    user_df = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/login_details.xlsx',sheet_name='Login_Details')
    user_match = user_df.loc[user_df['Employee_ID']==emp_id]

    url = "https://dev78375.service-now.com/api/now/table/incident"

    username = "admin"
    password = "9%3fWxi^LiWW"

    # JSON payload for creating an Incident

    incident_payload = {
        "short_description": result_df['Short_Description'].iloc[0],
        "description": result_df['Description'].iloc[0],
        "caller_id": user_match['Employee_ID'].iloc[0],
        "caller_number":user_match['Phone_Number'].iloc[0],
        "category":result_df['Category'].iloc[0],
        "subcategory":result_df['SubCatagory'].iloc[0],
        "configuration_item":result_df['Configuration_Item'].iloc[0],
        "assignment_group":result_df['Assignment_Group'].iloc[0]
        # Add more fields as needed

    }

    # Set up authentication
    auth = (username, password)
    # Send POST request to create an Incident
    response = requests.post(url, json=incident_payload, auth=auth)

    # Check response
    if response.status_code == 201:
        return response.json().get("result").get("number")
    else:
        return ("Contact Administrator: Check Service Now instance")#response.text

# def main():
#     Incident("vdi is slow")

# if __name__ == "__main__":
#     main()