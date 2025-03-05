# Git Watcher

## Overview
This repository holds the core python code files for git watcher task on merge action on repo. planned out and created by Andrew Chou.

## Table of Contents
- [Features](#features)
- [Installation Steps](#installation-steps)
- [Slack Setup](#setting-up-slack-token)
- [Scheduling](#setting-task-scheduling)
- [Project Structure](#project-structure)
- [Component](#components)
- [Others](#others)

## Features
1. Using Github API to retreive the event on merge or pull requests.
2. Using Slack API to send message to slack channel.\
3. Send alert to Slack Channel to notify git pull action to users.
4. Periodically Task Running through Github Actions Workflow to frequently detect merge action so users are being notified in real-time.
5. Error Logging to app.log file for debugging purposes.

## Installation Steps
1. Clone the repository:
    ```bash
    git clone 
    ```
2. Set up virtual environment
    ```bash
    python -m venv venv
    ```
    - Windows:
    ```bash
    venv\Scripts\activate
    ```

    - macOS:
    ```bash
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Setup .gitignore:
    - Place "\venv" and ".env" in it

## Setting up Slack Token
- Visit Slack API page at https://api.slack.com
    - Make sure to log in to slack account
- Click "Create New App" -> "From Scratch", then enter the details such as:
    - Name for the App
    - Slack workspace to add the app in
- Add OAuth Scopes for the App:
    - Left-hand menu, click "OAuth & Permissions"
        - Find "Bot Token Scopes", and Add the following scopes:
            - chat:write (to send message)
            - chat:write.public (to mention everyone)
        - Then scroll up to "OAuth Tokens" and click "Install App to Workspace"
            - Click "Allow" if receiving any prompt
**Note:** Save the "Bot User OAuth Token", and paste it to SLACK_TOKEN in .env
- Add the bot to the channel that need to be added in:
    - Go to the channel and in the chat box, type:
        ```plaintext
        /invite @YourBotName
        ```

## Setting Task Scheduling
- Currently, the periodic task scheduling is being hosted on Github Actions Workflow
    - The default setup are configured in .github/workflows/polling.yml
        - Nothing needs to be made change to it, the current setup is to check once every 30 minutes (But there will be some delay to it)
        - The frequency can be changed in the "cron" portion in the yml!


## Project Structure
```plaintext
GIT-WATCHER
├── .github/workflows            # Main github action workflow setup
│   ├── watchdog.yml              # yml script to define cron scheduling and tasks for github action
├── watchdog.py                   # Python Script for the main task
├── app.log                      # Error and events log (to be created when first running the script)
├── README.md                    # Readme + Details
├── requirements.txt             # list of packages being installed to make the python script work
```

## Components
- **.github/workflows/**: Contain the basic config for cron scheduling setup.

## Others
- NA