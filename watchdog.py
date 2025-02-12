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
slack_channel_id = ''

# initialize slack client
client = WebClient(token=slack_token)

# github repo setup
GITHUB_OWNER = ""
GITHUB_REPO = ""
GITHUB_TOKEN = os.environ("GITHUB_TOKEN")
MERGE_FILE = "merge_log.txt" # to prevent repetitive merge alert

# github api setup
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# will use github api directly to perform get request for all git events
# return boolean to detect if merge event found!
def detect_merge(branch):
    # setup url
    url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/pulls?state=closed&sort=updated&direction=desc"
    response = requests.get(url, headers=HEADERS) # perform request
    return trigger


# once getting the trigger status --> send notification to slack directly
# using trigger to detect notif action
def send_notif(branch, trigger):
    try:
        # For sending alert both working and non working status
        message = ""
        if trigger:
            message = f"<!channel> ‼️ Merge actions are detected, Please make sure to perform git pull on the branch {branch} before proceeding with any updates."
        # else:
        #     message = f"<!channel> No merge detected!"
        client.chat_postMessage(channel=slack_channel_id, text=message)
        logger.info(f"Sent alert to Slack: {message}")
    except SlackApiError as e:
        logger.error(f"Error to post message to Slack channel {slack_channel_id}: {e.response['error']}")