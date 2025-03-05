"""
watchdog.py

This files is for doing backend to detect any git merge action to the repo

Author: Andrew Chou
Date Created: 02/10/2025

Dependencies:
- requests: HTTP library for making HTTP requests.
- logging: for logging error or event messages (save to app.log)
- slack_sdk: tool for connecting python script to slack channel
"""

import requests
import logging
from logging.handlers import RotatingFileHandler

import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# Configure logging with rotating file handler base on size
# setting logging file with rotation when size exceed happen
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)

# Setup logger
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Load environment variables for slack 
slack_token = os.environ['SLACK_TOKEN']
slack_channel_id = os.environ['SLACK_CHANNEL']

# initialize slack client
client = WebClient(token=slack_token)

# github repo setup
GITHUB_OWNER = "247teach"
GITHUB_REPO = "naomi-nextjs-app"
GITHUB_TOKEN = os.environ.get("NAOMI_GITHUB_TOKEN")
MERGE_FILE = "merge_log.txt" # to prevent repetitive merge alert
last_merge_pr = None # to be used to detect if notif is made yet
pr_link = None # to be used for pr link referencing

# github api setup
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# # for testing github api for the first time
# def get_recent_events():
#     url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls?state=closed&sort=updated&direction=desc"
    
#     try:
#         response = requests.get(url, headers=HEADERS)
#         response.raise_for_status()  # Raise an error if the request fails

#         # Debug: Print response headers
#         print("Response Headers:", response.headers)
        
#         pulls = response.json()

#         # Debug: Check if the response is empty
#         if not pulls:
#             logger.info("No closed pull requests found.")
#             print("No closed PRs found. Full Response:", response.text)
#             return "No closed PRs found."

#         # Debugging: Print the raw API response
#         print("Raw API Response (First PR):", pulls[0] if pulls else "No PRs")

#         # Filter only merged PRs
#         merged_pulls = [pr for pr in pulls if pr.get("merged_at")]

#         if not merged_pulls:
#             logger.info("No merged pull requests found.")
#             print("No merged PRs found.")
#             return "No merged PRs found."

#         # Print first 5 merged PRs
#         for i, pr in enumerate(merged_pulls[:5]):
#             title = pr.get("title", "Unknown Title")
#             created_at = pr.get("created_at", "Unknown Date")
#             user = pr.get("user", {}).get("login", "Unknown User")
#             merged_at = pr.get("merged_at", "Unknown Date")

#             print(f"{i+1}. Merged PR: {title} | User: {user} | Created: {created_at} | Merged: {merged_at}")

#         return merged_pulls[:5]  # Return first 5 merged PRs
    
#     except requests.exceptions.RequestException as e:
#         logger.error(f"GitHub API error: {e}")
#         print(f"GitHub API error: {e}")
#         return None

# will use github api directly to perform get request for all git events
# return boolean to detect if merge event found!
def detect_merge(branch):
    global last_merge_pr # declare global variable
    global pr_link
    
    # create merge log if not exist!
    if not os.path.exists(MERGE_FILE):
        with open(MERGE_FILE, "w") as f:
            f.write("")
        
    # setup url
    # this will detect both merged and unmerged activity on the repo in questions
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls?state=closed&sort=updated&direction=desc"
    response = requests.get(url, headers=HEADERS) # perform request
    
    if response.status_code != 200:
        logger.error(f"Failed to get events from GitHub API: {response.status_code}")
        return False
    
    pulls = response.json()
    
    for pr in pulls:
        pr_number = str(pr.get("number"))
        pr_link = str(pr.get("html_url"))
        merged = pr.get("merged_at")
        base_branch = pr.get("base", {}).get("ref")
        # Check if the PR is merged
        # and must be on the branch I'm monitoring
        if merged and base_branch == branch:
            logger.info(f"Merge detected on branch {branch}!")
            last_merge_pr = pr_number
            return True
    logger.info(f"No merge detected on branch {branch}.")
    # print(f"No merge detected on branch {branch}.")
    return False

# return back boolean to tell if notification should be sent
def detect_notif():
    global last_merge_pr
    # prevent calling this function before detect_merge
    if not last_merge_pr:
        logger.info("No merge PR detected yet!")
        return False
    
    # read merge log file first
    if os.path.exists(MERGE_FILE):
        with open(MERGE_FILE, "r") as f:
            notified_pr = f.read().splitlines()
    else:
        notified_pr = []
    
    # check if current merge pr is in log file yet?
    if last_merge_pr in notified_pr:
        logger.info(f"PR #{last_merge_pr} already been notified!")
        return False

    # at this point, pr are newly merged --> send notif
    # add current pr to log file again
    with open(MERGE_FILE, "a") as f:
        f.write(last_merge_pr + "\n")
    # send_notif(last_merge_pr)
    return True # notification can be sent!

# once getting the trigger status --> send notification to slack directly
# using trigger to detect notif action
def send_notif(branch):
    # message = "testing slack config for git watch notification"
    # client.chat_postMessage(channel=slack_channel_id, text=message)
    global last_merge_pr
    global pr_link
    try:
        # Check if notification should be sent
        should_notify = detect_notif()
        
        if should_notify:
            # Pull request #94 has been merged into the main branch. Please run git pull before making further updates to ensure your local repository is up to date
            message = f"<!channel> Pull request `#{last_merge_pr}` ({pr_link}) has been merged into the `{branch}` branch. Please run `git pull` before making further updates to ensure your local repository is up to date"
            client.chat_postMessage(channel=slack_channel_id, text=message)
            logger.info(f"Sent alert to Slack: {message}")
        else:
            logger.info("No new merge detected. Notification not sent.")
    except SlackApiError as e:
        logger.error(f"Error posting message to Slack channel {slack_channel_id}: {e.response['error']}")

def run(branch):
    detect_merge(branch)
    detect_notif()
    #send_notif(branch)
    return   
        
# main function to run the script
if __name__ == "__main__":
    run("main")