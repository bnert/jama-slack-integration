import json
from jama import api_caller
from jama import tools as jama_tools
from slack.slack_json_factories.resp_json import bot
from flask import request, make_response
from slack import tools
import re

"""bot.py == Backbone of SlackBot functionality

There is one main functionaries present in this file:
    1. Receiving data from Slack conversation and response accordingly

As the file name is states, these functions are the backbone for the ability to response
a message from data that is input in Slack.

Attributes:
    None
"""

def event(base_url, payload, slack_client):
    """
    Process text from slack conversation and response message under the thread
    Filter out mmessage sent from SlackBot
    Find numerical data from text, conform them from Jama

    Args:
        base_url (string): The Jama workspace base_url
        payload (dict): payload receive from slack
        slack_client (SlackClient Object): to sent Slack message

    Returns:
        Response (object): To make the response, we use make_response()
    """
    if payload["event"].get("bot_id") or payload["event"].get("message", {}).get("bot_id"):
        return make_response("", 200)
    number = filter_number(payload["event"]["text"])
    teamID = tools.string_to_int(payload["team_id"])
    userID = tools.string_to_int(payload["event"]["user"])
    for num in number:
        jama_json_response = jama_tools.get_item_by_ID(base_url, num, teamID, userID)
        if jama_json_response["meta"]["status"] == "OK":
            item_mentioned(payload, jama_json_response, slack_client)
            continue

        jama_json_response = jama_tools.get_project_by_ID(base_url, num, teamID, userID)
        if jama_json_response["meta"]["status"] == "OK":
            project_mentioned(payload, jama_json_response, slack_client)
            continue
    return make_response("", 200)


def project_mentioned(payload, jama_json_response, sc):
    """
    Response message under the thread, when the message included projectID

    Args:
        payload (dict): payload receive from slack
        jama_json_response (dict): payload receive from jama
        sc (SlackClient Object): to sent Slack message

    Returns:
        Response (object): To make the response, we use make_response()
    """
    project_name = jama_json_response["data"]["fields"]["name"]
    projectID = jama_json_response["data"]["id"]
    sc.api_call(
        "chat.postMessage",
        channel=payload["event"]["channel"],
        thread_ts=payload["event"]["ts"],
        attachments=bot.project_response(projectID, project_name)
    )
    return make_response("", 200)


def item_mentioned(payload, jama_json_response, sc):
    """
    Response message under the thread, when the message included itemID

    Args:
        payload (dict): payload receive from slack
        jama_json_response (dict): payload receive from jama
        sc (SlackClient Object): to sent Slack message

    Returns:
        Response (object): To make the response, we use make_response()
    """
    item_name = jama_json_response["data"]["fields"]["name"]
    itemID = jama_json_response["data"]["id"]
    sc.api_call(
        "chat.postMessage",
        channel=payload["event"]["channel"],
        thread_ts=payload["event"]["ts"],
        attachments=bot.item_response(itemID, item_name)
    )
    return make_response("", 200)

def filter_number(text):
    number = re.findall(r"\d+", text)
    time = re.findall(r"\d+", " ".join(re.findall(r"(\d+:\d+)", text)))
    big_num = re.findall(r"\d+", " ".join(re.findall(r"(\d*[,]\d{3})", text)))
    ID = re.findall(r"\d+", " ".join(re.findall(r"(<@\w+>)", text)))
    for i in (time+big_num+ID):
        number.remove(i)
    return number
