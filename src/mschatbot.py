#!/usr/bin/env python3
# Charbel Kaed

""" Azure Bot Handler: Butlor """

import re
import json
import requests



global_ACCESS_TOKEN = ""
global_CONVERSATION_ID = ""
global_STREAM_URL = ""


def ask_butlor(cmd):
    """Sends Message to the Bot """

    if (not global_ACCESS_TOKEN) and (not global_CONVERSATION_ID):
        get_conversation_id()
    var_watermark = post_conversation(cmd)
    if var_watermark == -1:
        return "Sorry!! \n I don't have an answer right now"
    return get_answer(var_watermark)


def post_conversation(butlor_message):
    """ Post the message received from the User"""
    url = "https://directline.botframework.com/v3/directline/conversations/"+global_CONVERSATION_ID+"/activities"

    payload = "{\"type\": \"message\",\"from\":{\"id\": \"charbel\"},\"text\": \""+butlor_message+"\"}"
    headers = {'content-type': "application/json", 'authorization': "Bearer "+global_ACCESS_TOKEN+"", 'cache-control': "no-cache"}

    response = requests.request("POST", url, data=payload, headers=headers)
    data = json.loads(response.text)
    print(data)
    var_error = re.search('error', response.text)
    if var_error:
        var_token = re.search('TokenExpired', response.text)
        if var_token:
            #Force Global to null to referesh the token
            global global_ACCESS_TOKEN
            global_ACCESS_TOKEN = ""
            ask_butlor(butlor_message)
        print("error detected")
        return -1

    var_watermark = data['id']
    var_watermark = re.sub(global_CONVERSATION_ID+"|", "", var_watermark)
    return var_watermark


def get_answer(watermark):
    """ Retrieve the answer from the Butler """
    url = "https://directline.botframework.com/v3/directline/conversations/"+global_CONVERSATION_ID+"/activities?watermark="+watermark
    headers = {'content-type': "application/json", 'authorization': "Bearer "+global_ACCESS_TOKEN+"", 'cache-control': "no-cache"}

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    if data:
        var_activities = data['activities']
        if var_activities[0]:
            var_text = var_activities[0]['text']
            print(var_text)
    else:
        var_text = "Sorry unable to respond"

    return var_text




def get_conversation_id():
    """ Retrieves a Conversation ID """
    url = "https://directline.botframework.com/v3/directline/conversations"

    headers = {'authorization': "Bearer "+read_token_from_file()+"", 'cache-control': "no-cache"}

    response = requests.request("POST", url, headers=headers)
    print(response.text)
    data = json.loads(response.text)

    global global_CONVERSATION_ID
    global_CONVERSATION_ID = data['conversationId']

    global global_ACCESS_TOKEN
    global_ACCESS_TOKEN = data['token']

    print("Get Conversation "+global_CONVERSATION_ID)
    #global global_STREAM_URL
    #global_STREAM_URL = data['streamUrl']


def authenticate_ms_chatbot_directline():
    """Authenticate with MS Chatbot via DirectLine """

    headers = {'authorization': "Bearer "+read_token_from_file()+"", 'cache-control': "no-cache"}

    url = "https://directline.botframework.com/v3/directline/conversations"
    response = requests.request("POST", url, headers=headers)
    data = response.text
    print(data)
    global global_ACCESS_TOKEN
    global_ACCESS_TOKEN = json.loads(data)['token']

    global global_CONVERSATION_ID
    global_CONVERSATION_ID = json.loads(data)['conversationId']

    global global_STREAM_URL
    global_STREAM_URL = json.loads(data)['streamUrl']


def read_token_from_file():
    """ Read Token from file """
    var_token = open('/home/pi/ButlorVoiceKit/src/secret.txt', 'r').read()
    print(var_token)
    return var_token
