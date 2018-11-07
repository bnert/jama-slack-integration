import requests
from flask import request, Response
import json
import os
import time
import hmac
import hashlib
import base64
 
def return_to_slack(req, data):
    """
        Author: Jingyu
        Usage: Send data back to slack url given upon req
    """

    requests.post(req.form['response_url'], json=data, headers={'Content-Type': 'application/json'})
    return ""

def slack_sent_message(url, payload):
    """
        Usage: Send message back to slack via bot
    """
    header = {
        'Content-Type': 'application/json; charset=UTF-8', 
        "Authorization": "Bearer " + os.environ["SLACKBOT_TOKEN"]
    }
    response = requests.post(url, json=payload, headers=header)
    return response.text

def open_dialog_t(payload, trigger_id):
    """
        Author: Taisheng, Jingyu
        Usage: Open a dialog in slack
    """
    header = {
        "Content-Type": "application/json;charset=\"utf-8\"",
        "Authorization": "Bearer " + os.environ["SLACK_BOT_TOKEN"]
    }
    data = {
        "trigger_id": trigger_id,
        "dialog": payload
    }
    returnResult = requests.post("https://slack.com/api/dialog.open", json=data, headers=header)
    print(returnResult.text)
    return ""

def verify(request):
    try:
        secret = os.environ["SLACK_SIGNING_SECRET"].encode("UTF-8")
        slacksig = request.headers["X-Slack-Signature"]
        timestamp = request.headers["X-Slack-Request-Timestamp"]
    except:
        return False

    body = request.get_data()

    # if the request is reportedly from more than five minutes ago,
    # reject because it's either an attack or of no use at this point
    currentTime = int(time.time())
    if(currentTime - int(timestamp) > 60*5):
        return False

    basebytes = "v0:" + timestamp + ":"
    basebytes = basebytes.encode("UTF=8") + body

    signature = hmac.digest(secret, basebytes, hashlib.sha256).hex()
    return hmac.compare_digest(slacksig[3:], signature)

def string_to_int(payload):
    """
        Author: Jingyu
        Usage: return a integer from a string, if the string is not a int, return -1 as error code.
    """
    try:
        ret = int(payload)
    except ValueError:
        ret = -1
    return ret

def prepare_html(payload):
    """
    replace the user input with correct html code. so that we can submit the data to Jama in an expected format
    @params:
        payload -> user input
    """
    return payload.replace('\n', '<br>')

def prepare_jama_mention(jama_user_info):
    """
    Make a html block of jama's @mention functionality
    @params:
        ama_user_info -> The user data get from jama's REST API /users
    """
    full_name = jama_user_info["firstName"] + " " + jama_user_info["lastName"]
    user_id = str(jama_user_info["id"])
    return "<span contenteditable='false' data-j-object='User:" + user_id + "' data-j-type='User' data-j-name='" +\
           full_name + "' data-j-key='" + jama_user_info["username"] + "' data-j-id='" + user_id +\
           "' class='js-at-mention-key at-mention-key js-at-mention-user at-mention-user'>" + full_name + "</span>"

def get_file(download_url):
    """
    Get a file from slack
    @params:
        download_url -> the down url of the file, If you got a json from slack massage, please use the
                        "url_private_download" link.
    """
    response = requests.get(download_url, allow_redirects=True, headers={"Authorization": "Bearer " + os.environ["SLACK_OAUTH_TOKEN"]})
    return response.content

def cutArgument(input, indicator):
    """
    To cut an input into two argument
    @params:
        input -> input data
        indicator -> the indicator char of where you wan to split the input
    """
    result = input.split(indicator, 1)
    if len(result) < 1:
        return "", ""
    elif  len(result) < 2:
        return result[0], ""
    return result[0], result[1]
