import os
import requests
from flask import make_response
from flask import request
from slackclient import SlackClient

from jama import search
from jama import comment
from jama import oauth
from jama.tools import user_error
from jama.tools import make_dict
from jama.tools import commands_info
from slack import tools

from slack.slack_json_factories import oauth_dialog_json

from .resolvers import *

"""Purpose: handle routing to different funcitonality
Here are the key secitons in this file:
    1. Handlers for /jama/dialog
    2. Handlers for /jama/menu
    3. Handlers from /jama
    4. High-level Resolvers for comment, oauth, search

Each of the url parameters are used in the following way:
    a. /jama/dialog: To handle dialog submission data.
    b. /jama/menu: To handle interactive components for jama dialogs.
    c. /jama: Main intake endpoint for slash commands.
    d. Resolvers: Layer of abstractions to decide where to send data for each piece of functionality.

Attributes:
    os.environ(['SLACK_BOT_TOKEN']) (String): String containing the SLACK_BOT_TOKEN,
    a string in the environment variables.

    slack_client (SlackClient object): From the Slack module, we initialize
        slack_client with our Slack bot token, given using api.slack.com
"""

slack_client = SlackClient(os.environ['SLACK_BOT_TOKEN'])


# Verification
def verify_req(req):
    """Verifies the passed in request has been sent from Slack

    Arguments:
        req (Request object): Required

    Returns:
        bool: True for success, False for deny.
    """
    if "SLACK_SIGNING_SECRET" in os.environ:
        if(not tools.verify(req)):
            print("Verification failed")
            return False
    else:
        print("WARNING: No signing secret provided, so no verification of slack requests will be done. This is a HUGE SECURITY RISK!")
        print("I definitely agree with this error message - Brent")
    return True


# Handlers for /jama/dialog

def resolve_dialog_submit(base_url, payload):
    """Resolves where to pass of a dialog submission from Slack.

    Arguments:
        base_url (string): The base a Jama URL
        payload (JSON Object): Payload from dialog submission

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """
    
    if not payload:
        print("OH NO")
        return make_response("", 500)

    if payload["type"] == "dialog_submission":
        if payload["callback_id"] == "jamaconnect_create_dialog":
            return create_dialog.resolve_submit(base_url, payload)
        elif payload["callback_id"] == "comment":
            return comment_dialog.resolve_submit(base_url, payload)
        elif payload["callback_id"] == "attachment":
            return attachment_dialog.resolve_submit(base_url, payload)
        elif payload["callback_id"] == "search":
            return search_dialog.resolve_submit(base_url, payload)
        elif payload["callback_id"] == "display":
            print("reached display thru dialog")
            return display_dialog.resolve_submit(base_url, payload)
        elif payload["callback_id"] == "oauth":
            requests.post(payload["response_url"],
                          json={ "text": oauth.receive_dialog(payload) },
                          headers={"Content-Type": "application/json"})
            return make_response("", 200)

        else:
            return make_response("", 500)

    if payload["type"] == "message_action":
        if payload["callback_id"] == "attachment":
            return attachment_action.resolve_submit(payload, slack_client)
        elif payload["callback_id"] == "comment":
            return comment_action.resolve_submit(payload, slack_client)
    else:
        return make_response("", 500)


# Handlers for /jama/menu/
def resolve_menu_req(base_url, payload):
    """
    @params:
        url -> url to send data to
        payload -> json to pass off
    """
    if not payload:
        print("OH NO")
        return make_response("", 500)

    if payload["type"] == "dialog_suggestion":
        if payload["callback_id"] == "comment":
            return comment.dialog_option(base_url, payload)
        else:
            return make_response("", 500)


# Handlers for /jama/

##### Resolvers for /jama/

def resolve_jama_req(base_url, req):
    """Resolves where to pass of requests made the /jama.

    Arguments:
        base_url (string): The base a Jama URL
        payload (JSON Object): Payload from dialog submission

    Returns:
        Response (object): To make the response, we use make_response()
        from the flask library.
    """

    # req.form = args from slash command
    print(tools.cutArgument(req.form['text'], ':'))
    action, content = tools.cutArgument(req.form['text'], ':')
    print("Action: " + action)
    print("Content: " + content)
    action = action.strip().lower()
    content = content.strip()

    # See's what kind of arguments there are
    if(action == 'search'):
        print('SEARCH')
        return search_req.resolve(base_url=base_url,
                                content=content,
                                slack_client=slack_client,
                                request=request)

    elif(action == 'display'):
        print('DISPLAY')
        return display_req.resolve(base_url=base_url,
                                content=content,
                                slack_client=slack_client,
                                request=request)

    elif 'create' in action:
        if (content == ""):
            try:
                content = action.split(' ')[1]
                content = content.strip()
                content = int(content)
            except:
                return commands_info.create(request,
                headline="There was an error with your inputs!")

        return create_req.resolve(base_url=base_url, 
                                content=content,
                                slack_client=slack_client,
                                request=request)

    elif (action == 'comment'):
        print('COMMENT')
        return comment_req.resolve(base_url=base_url,
                                   content=content,
                                   slack_client=slack_client,
                                   request=request)

    elif (action == 'oauth'):
        print('OAUTH')
        return resolve_oauth_req(request, content)

    elif (action == 'help'):
        print('HELP')
        return resolve_help_req(content)

    else:
        # If input from user is buggy
        content = req.form["text"].strip()
        if "comment" in content:
            return commands_info.comment(request)
        elif "create" in content:
            return commands_info.create(request,
            headline="There was an error with your command! Here is a quick guide to using `/jamaconnect create`:")
        elif "search" in content:
            return commands_info.search(request)
        else:
            return commands_info.all(request)


### Resolver functions

def resolve_oauth_req(req, content):
    """
    @params:
        req -> Request to process
        content -> Arguments from Slack user
    """
    try:
        if content == "":
            slack_client.api_call("dialog.open",
                                  trigger_id=request.form["trigger_id"],
                                  dialog=oauth_dialog_json.oauth_dialog())
            return make_response("", 200)

        content = make_dict(content)
        return oauth.add_credentials(request.form["team_id"],
                                     request.form["user_id"],
                                     content["id"],
                                     content["secret"])
    except Exception as e:
        print(e)
        return make_response("Invalid input! Usage: /jamaconnect oauth: id=[your client ID], secret=[your client secret] (or just \"/jamaconnect oauth\" for an interactive dialog)", 200)


def resolve_help_req(content):
    try:
        return help.help(content)
    except Exception as e:
        print(e)
        return commands_info.all(request)
