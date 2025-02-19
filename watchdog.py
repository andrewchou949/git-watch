"""
watchdog.py

This files is for doing backend to detect any git merge action to the repo

Author: Andrew Chou
Date Created: 02/10/2025

Dependencies:
- requests: HTTP library for making HTTP requests.
- time: for setting interval (not being used yet!)
- logging: for logging error or event messages (save to app.log)
- dotenv: library for loading env variable.
- slack_sdk: tool for connecting python script to slack channel
"""

import requests
import logging
from logging.handlers import RotatingFileHandler

import os
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError


# Configure logging with rotating file handler base on size
# setting logging file with rotation when size exceed happen
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)

# Setup logger
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# # Load environment variables for slack 
# slack_token = os.environ['SLACK_TOKEN']
# slack_channel_id = ''

# # initialize slack client
# client = WebClient(token=slack_token)

# github repo setup
GITHUB_OWNER = "andrewchou949"
GITHUB_REPO = "Personal-Finance-Management-Application"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
MERGE_FILE = "merge_log.txt" # to prevent repetitive merge alert

# github api setup
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# for testing github api for the first time
def get_recent_events():
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls?state=closed&sort=updated&direction=desc"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an error if the request fails

        # Debug: Print response headers
        print("Response Headers:", response.headers)
        
        pulls = response.json()

        # Debug: Check if the response is empty
        if not pulls:
            logger.info("No closed pull requests found.")
            print("No closed PRs found. Full Response:", response.text)
            return "No closed PRs found."

        # Debugging: Print the raw API response
        print("Raw API Response (First PR):", pulls[0] if pulls else "No PRs")

        # Filter only merged PRs
        merged_pulls = [pr for pr in pulls if pr.get("merged_at")]

        if not merged_pulls:
            logger.info("No merged pull requests found.")
            print("No merged PRs found.")
            return "No merged PRs found."

        # Print first 5 merged PRs
        for i, pr in enumerate(merged_pulls[:5]):
            title = pr.get("title", "Unknown Title")
            created_at = pr.get("created_at", "Unknown Date")
            user = pr.get("user", {}).get("login", "Unknown User")
            merged_at = pr.get("merged_at", "Unknown Date")

            print(f"{i+1}. Merged PR: {title} | User: {user} | Created: {created_at} | Merged: {merged_at}")

        return merged_pulls[:5]  # Return first 5 merged PRs
    
    except requests.exceptions.RequestException as e:
        logger.error(f"GitHub API error: {e}")
        print(f"GitHub API error: {e}")
        return None


# will use github api directly to perform get request for all git events
# return boolean to detect if merge event found!
def detect_merge(branch):
    # setup url
    # this will detect both merged and unmerged activity on the repo in questions
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls?state=closed&sort=updated&direction=desc"
    response = requests.get(url, headers=HEADERS) # perform request
    
    if response.status_code != 200:
        logger.error(f"Failed to get events from GitHub API: {response.status_code}")
        return False
    
    pulls = response.json()
    
    for pr in pulls:
        # Check if the PR is merged
        # and must be on the branch I'm monitoring
        if pr.get("merged_at") and pr.get("base", {}).get("ref") == branch:
            logger.info(f"Merge detected on branch {branch}!")
            print(f"Merge detected on branch {branch}!")
            return True
    logger.info(f"No merge detected on branch {branch}.")
    print(f"No merge detected on branch {branch}.")
    return False


# # once getting the trigger status --> send notification to slack directly
# # using trigger to detect notif action
# def send_notif(branch, trigger):
#     try:
#         # For sending alert both working and non working status
#         message = ""
#         if trigger:
#             message = f"<!channel> ‼️ Merge actions are detected, Please make sure to perform git pull on the branch {branch} before proceeding with any updates."
#         # else:
#         #     message = f"<!channel> No merge detected!"
#         client.chat_postMessage(channel=slack_channel_id, text=message)
#         logger.info(f"Sent alert to Slack: {message}")
#     except SlackApiError as e:
#         logger.error(f"Error to post message to Slack channel {slack_channel_id}: {e.response['error']}")
        
        
# main function to run the script
if __name__ == "__main__":
    # get recent events
    events = detect_merge("main")
    if events:
        print("Events found!")
    else:
        print("Failed! No events found.")