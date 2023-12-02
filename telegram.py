#!/usr/bin/env python
'''Import requirements'''
import argparse
import json
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
import logging
import requests
import os
import sys

__author__ = 'Kanishk Singh (Arion Miles)'
__license__ = "MIT"

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

logger = logging.getLogger()
handler = logging.FileHandler(os.path.join(__location__, 'notifications.log'))
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Settings
check_creds = os.path.isfile(os.path.join(__location__, 'creds.ini'))
if check_creds:
    CONFIG = configparser.ConfigParser()
    CONFIG.read(os.path.join(__location__, 'creds.ini'))
    API_KEY_TOKEN = CONFIG.get('CREDS', 'API_TOKEN')
    CHAT_ID = CONFIG.get('CREDS', 'CHAT_ID')
else:
    print("Error: creds.ini not found")        
    sys.exit()

PARSER = argparse.ArgumentParser(description="Filebot report tool.")
PARSER.add_argument('-title', '-t', type=str, help="Message title", required=False)
PARSER.add_argument('-message', '-m', type=str, help="Message content", required=False, default="")
ARGS = PARSER.parse_args()

def telegram(message_title, message_content):
    '''Submit message to Telegram via Bot'''
    CONTENT = message_title + '\n' + message_content

    # Defining the api-endpoint
    API_ENDPOINT = "https://api.telegram.org/bot" + API_KEY_TOKEN + "/sendMessage"

    # Data to be sent to API
    DATA = {'text':CONTENT,
        'chat_id':CHAT_ID,
        'parse_mode': 'html'}

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
