# Polling on Naomi Endpoint

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
1. [placeholder]

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
- [placeholder]

## Setting Task Scheduling
- [placeholder]


## Project Structure
```plaintext
GIT-WATCHER
├── .github/workflows            # Main github action workflow setup
│   ├── polling.yml              # yml script to define cron scheduling and tasks for github action
├── polling.py                   # Python Script for monitoring health of endpoints
├── app.log                      # Error and events log (to be created when testing the endpoint)
├── README.md                    # Readme + Details
├── requirements.txt             # list of packages being installed to make the python script work
```

## Components
- **.github/workflows/**: Contain the basic config for cron scheduling setup.

## Others
- If new endpoints need to be added, make sure to add them in the **main** section's "endpoints" list.
    - Be sure to include default input info to be feed in the endpoint to prevent unnecessary errors.
- Sometimes the cron scheduling on github action workflow may fail with code 500 due to high traffic at the time, to further check or troubleshoot if the issue is from 500 or something else, need to manually run the polling again.
    - Below is the step to manual run the cron on github
        - Go to https://github.com/247teach/naomi-polling-api
        - Click on "Actions" tab and on left side menu, click "Polling Script Scheduler"
        - There will be a "Run workflow" drop down menu on the right side header
        - Click the green "Run workflow" button from the drop down
    **Note**: If there's an error message on slack's "Naomi-test" channel -> this indicate issue with API
    Otherwise, there should not be any error message on the channel when running -> the API is working fine, the issue encountered previously is indeed due to high traffic flow during the time