#!/usr/bin/env python
'''Import requirements'''
import argparse
import json
import configparser
import logging
import requests
import os
import sys

__author__ = 'Kanishk Singh (Arion Miles)'
__license__ = "MIT"

# Get the path - checking to see if we're compiled or not
def resolve_path(path):
    if getattr(sys, "frozen", False):
        # When running from a compiled executable, get the path of the executable itself
        resolved_path = os.path.abspath(os.path.join(sys._MEIPASS, path))
    else:
        # When running from the command line, get the path of the current script's directory
        resolved_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    resolved_path = resolved_path + "/" + path
    return resolved_path

# Set up Logging
if not os.path.exists(resolve_path("notifications.log")):
    # If the file does not exist, create it
    open(resolve_path("notifications.log"), 'a').close()
logger = logging.getLogger()
handler = logging.FileHandler(resolve_path("notifications.log"))
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Get Settings
if not os.path.exists(resolve_path("creds.ini")):
    # If creds.ini doesn't exist, create it in the same directory as the script
    CONFIG = configparser.ConfigParser()
    CONFIG.add_section('CREDS')
    CONFIG.set('CREDS', 'API_TOKEN', 'YOUR_API_TOKEN_HERE')
    CONFIG.set('CREDS', 'CHAT_ID', 'YOUR_CHAT_ID_HERE')
    with open(resolve_path("creds.ini"), 'w') as file:
        CONFIG.write(file)
    print("Error: You need to update creds.ini with your credentials")        
    sys.exit()
CONFIG = configparser.ConfigParser()
CONFIG.read(resolve_path("creds.ini"))
API_KEY_TOKEN = CONFIG.get('CREDS', 'API_TOKEN')
CHAT_ID = CONFIG.get('CREDS', 'CHAT_ID')

# Get Command Line Arguments
PARSER = argparse.ArgumentParser(description="TelegramBot")
PARSER.add_argument('-title', '-t', type=str, help="Title", required=False)
PARSER.add_argument('-message', '-m', type=str, help="Message Content", required=False, default="")
ARGS = PARSER.parse_args()

# Submit message to Telegram via Bot
def telegram(message_title, message_content):
    '''Submit message to Telegram via Bot'''
    CONTENT = message_title + '\n' + message_content

    # Defining the api-endpoint
    API_ENDPOINT = "https://api.telegram.org/bot" + API_KEY_TOKEN + "/sendMessage"

    # Data to be sent to API
    DATA = {'text':CONTENT, 'chat_id':CHAT_ID, 'parse_mode': 'html'}

    # Sending post request and saving response as response object
    R = requests.post(url=API_ENDPOINT, data=DATA)
    STATUS = str(R.status_code)
    DICT = json.loads(R.text)
    OK = str(DICT['ok'])
    if "error_code" in DICT:
        ERR_CODE = str(DICT['error_code'])

    # Extracting response text
    if R.status_code == 200:
        logger.info('Message sent!')
    else:
        logger.info('OK: ' + OK + '| Error: ' + ERR_CODE + '| Description: ' + DICT['description'])

if __name__ == '__main__':
    message_title = ARGS.title
    message_content = ARGS.message
    telegram(message_title, message_content)