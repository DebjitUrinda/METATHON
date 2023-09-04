import requests

# ServiceNow API endpoint and credentials

def RITM():
    url = "https://dev78375.service-now.com/api/now/table/sc_req_item"
    username = "admin"
    password = "9%3fWxi^LiWW"
   
    # JSON payload for creating an Incident
    ritm_payload = {
    "configuration_item":"DP00288",
    "assignment_group":"database",
    "short_description":"RITM_testing",
    "description":"RITM_testing",
    "sys_created_by":"",
    "contact_type": "",
    "context": "ritm",
    "cat_item": "Access",
    "request": "REQ0010001",
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
    
def main():
    result=RITM()
    print(result)

if __name__ == "__main__":
    main()