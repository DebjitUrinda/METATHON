import requests

# ServiceNow API endpoint and credentials
def Ritm():
    url_REQ = "https://dev78375.service-now.com/api/now/table/sc_request"
    username = "admin"
    password = "9%3fWxi^LiWW"
    # JSON payload for creating an Incident
    req_payload = {
      "short_description":"RITM_testing",
      "description":"RITM_testing",
    }  
    # Set up authentication
    auth = (username, password)
   
    # Send POST request to create an Incident
    response_REQ = requests.post(url_REQ, json=req_payload, auth=auth)
     
    # Check response
    if response_REQ.status_code != 200:
       # print("RITM created successfully!")
        return(response_REQ.json())
    else:
        return(response_REQ.text)