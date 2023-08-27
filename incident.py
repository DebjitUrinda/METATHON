import requests

# ServiceNow API endpoint and credentials
def Incident():
    url = "https://dev78375.service-now.com/api/now/table/incident"

    username = "admin"
    password = "9%3fWxi^LiWW"

    # JSON payload for creating an Incident

    incident_payload = {
        "short_description": "Incident Testing",
        "description": "Incident Testing",
        "caller_id": "User ID or Email",
        # Add more fields as needed

    }

    # Set up authentication
    auth = (username, password)
    # Send POST request to create an Incident
    response = requests.post(url, json=incident_payload, auth=auth)

    # Check response
    if response.status_code == 201:
        #print("Incident created successfully!" + response.json())
        return response.json().get("result").get("number")
    else:
        return response.text
