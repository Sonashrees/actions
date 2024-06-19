import os
import requests
from requests.auth import HTTPBasicAuth
import json

# Retrieve and print environment variables (excluding sensitive information)
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_URL = os.getenv('JIRA_URL')

if not JIRA_API_TOKEN or not JIRA_USERNAME or not JIRA_URL:
    raise ValueError("One or more required environment variables are missing: JIRA_API_TOKEN, JIRA_USERNAME, JIRA_URL")

print(f"JIRA_URL: {JIRA_URL}")
print(f"JIRA_USERNAME: {JIRA_USERNAME}")

# Define the issue key and the field to monitor (adjust these as needed)
ISSUE_KEY = 'NW-167'  # Replace with your actual issue key
FIELD_TO_MONITOR = 'customfield_10213'  # Replace with your actual custom field ID
DESIRED_FIELD_VALUE = 'CC-CI-2024-01-08'  # Replace with the actual value you are monitoring for

# Define the subtask details
SUBTASK_SUMMARY = 'Automatically created subtask'
SUBTASK_DESCRIPTION = 'This subtask was automatically created based on the field value.'

# Function to get the issue details
def get_issue_details(issue_key):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"
    auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_API_TOKEN)
    headers = {
       "Accept": "application/json"
    }
    response = requests.request("GET", url, headers=headers, auth=auth)

    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")

    if response.status_code != 200:
        raise Exception(f"Failed to fetch issue details: {response.status_code} - {response.text}")
    
    return response.json()

# Function to create a subtask
def create_subtask(parent_issue_key):
    url = f"{JIRA_URL}/rest/api/3/issue"
    auth = HTTPBasicAuth(JIRA_USERNAME, JIRA_API_TOKEN)
    headers = {
       "Content-Type": "application/json"
    }
    payload = json.dumps({
        "fields": {
           "project": {
              "key": parent_issue_key.split('-')[0]
           },
           "parent": {
              "key": parent_issue_key
           },
           "summary": SUBTASK_SUMMARY,
           "description": {
              "type": "doc",
              "version": 1,
              "content": [
                 {
                    "type": "paragraph",
                    "content": [
                       {
                          "text": SUBTASK_DESCRIPTION,
                          "type": "text"
                       }
                    ]
                 }
              ]
           },
           "issuetype": {
              "name": "Sub-task"
           }
        }
    })
    response = requests.request("POST", url, headers=headers, data=payload, auth=auth)

    print(f"Subtask creation response status code: {response.status_code}")
    print(f"Subtask creation response content: {response.text}")

    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to create subtask: {response.status_code} - {response.text}")

    return response.json()

# Main script logic
try:
    issue_details = get_issue_details(ISSUE_KEY)
    field_value = issue_details['fields'].get(FIELD_TO_MONITOR)
    
    if field_value == DESIRED_FIELD_VALUE:
        subtask_response = create_subtask(ISSUE_KEY)
        print(f"Subtask created: {subtask_response}")
    else:
        print(f"Field value does not match: {field_value}")
except Exception as e:
    print(f"An error occurred: {e}")
