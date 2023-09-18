import requests
import pandas as pd

# ServiceNow API endpoint and credentials
def Incident(inc_argument,emp_id):
    inc_df = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/RITM_INC_CHG-Details.xlsx',sheet_name='INC_Sheet')
    inc_df["Short_Description"] = inc_df["Short_Description"].str.replace('.','',regex=False)
    inc_df_unique = inc_df.drop_duplicates(subset=['Short_Description'])
    inc_argument=inc_argument.replace('.','')
    result_df = inc_df_unique[inc_df_unique['Short_Description']==inc_argument]

    user_df = pd.read_excel('/Users/dbjt_baki/Desktop/Data_Engineering/Metathon/METATHON/login_details.xlsx',sheet_name='Sheet1')
    user_match = user_df[user_df['Employee_ID']==int(emp_id)]
    # print(type(user_match))
    # print(user_match)
# =============================================================================
#     print("Inside:")
#     print(user_match)
#     print(user_df.head(5))
#     print('HI!!!')
#    
    # print(str(result_df['Short_Description'].iloc[0]))
    # print(str(result_df['Description'].iloc[0]))
    # print(str(result_df['Category'].iloc[0]))
    # # print(str(result_df['SubCatagory'].iloc[0]))
    # # print(str(result_df['Configuration_Item'].iloc[0]))
    # print(str(result_df['Assignment_Group'].iloc[0]))
    # print(str(user_match['Full_Name'].iloc[0]))
#     # Add more fields as needed
# =============================================================================

    url = "https://dev78375.service-now.com/api/now/table/incident"

    username = "admin"
    password = "9%3fWxi^LiWW"

    # JSON payload for creating an Incident
    field1 = str(result_df['Short_Description'].iloc[0])
    field2 = str(result_df['Description'].iloc[0])
    field3 = str(result_df['Category'].iloc[0])
    field4 = str(result_df['Assignment_Group'].iloc[0])
    field5 = str(user_match['Full_Name'].iloc[0])
    field6 = str(result_df['SubCatagory'].iloc[0])

    incident_payload = {
        "short_description": field1,
        "description": field2,
        "category": field3,
        "assignment_group": field4,
        "caller_id": field5,
        "subcategory": field6
        # Add more fields as needed

    }

    # Set up authentication
    auth = (username, password)
    # Send POST request to create an Incident
    response = requests.post(url, json=incident_payload, auth=auth)

    print(response.status_code)

    # Check response
    if response.status_code == 201:
        return response.json().get("result").get("number")
    else:
        return ("Contact Administrator: Check Service Now instance")#response.text

# def main():
#     #Incident("vdi is slow","888468")
#     print(Incident("vdi is slow","870840"))

# if __name__ == "__main__":
#     main()
