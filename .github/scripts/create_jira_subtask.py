import os
import requests
from requests.auth = HTTPBasicAuth

# Retrieve and print environment variables (excluding sensitive information)
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_URL = os.getenv('JIRA_URL')

if not JIRA_API_TOKEN or not JIRA_USERNAME or not JIRA_URL:
    raise ValueError("One or more required environment variables are missing: JIRA_API_TOKEN, JIRA_USERNAME, JIRA_URL")

print(f"JIRA_URL: {JIRA_URL}")
print(f"JIRA_USERNAME: {JIRA_USERNAME}")

# Define a known issue key
KNOWN_ISSUE_KEY = 'NW-166'  # Replace with a known existing issue key

# Function to get the issue details
def get_issue_details(issue_key):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"
    auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_API_TOKEN)
    headers = {
       "Accept": "application/json"
    }
    response = requests.request("GET", url, headers=headers, auth=auth)

    print(f"Request URL: {url}")
    print(f"Request Headers: {headers}")
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")

    if response.status_code != 200:
        raise Exception(f"Failed to fetch issue details: {response.status_code} - {response.text}")
    
    return response.json()

# Main script logic
try:
    issue_details = get_issue_details(KNOWN_ISSUE_KEY)
    print(f"Issue details: {issue_details}")
except Exception as e:
    print(f"An error occurred: {e}")
