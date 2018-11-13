import os
import json
import requests
import threading
from flask import make_response
from flask import request
from slackclient import SlackClient

from jama import search
from jama import comment
from jama import oauth
from jama import attachment
from jama.tools import user_error
from jama.tools import make_dict
from jama.tools import commands_info
from slack import tools

from slack.slack_json_factories import item_dialog_json
from slack.slack_json_factories import comment_dialog_json
from slack.slack_json_factories import attachment_dialog_json
from slack.slack_json_factories import attachment_response_json
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
            requests.post(payload["response_url"],
                          json=comment.from_dialog_comment(base_url, payload),
                          headers={"Content-Type": "application/json"})
            return make_response("", 200)

        elif payload["callback_id"] == "attachment":
            thread = threading.Thread(target=attachment.dialog_attachment_thread,
                                      kwargs={"base_url": base_url, "data": payload})
            thread.start()
            return make_response("", 200)

        elif payload["callback_id"] == "oauth":
            requests.post(payload["response_url"],
                          json={ "text": oauth.receive_dialog(payload) },
                          headers={"Content-Type": "application/json"})
            return make_response("", 200)

        else:
            return make_response("", 500)

    if payload["type"] == "message_action":
        if payload["callback_id"] == "attachment":
            dialog = attachment_dialog_json.attachment_dialog(payload)
            if dialog is None:
                requests.post(payload["response_url"],
                              json=attachment_response_json.file_failure_response(),
                              headers={"Content-Type": "application/json"})
                return make_response("", 200)
            else:
                slack_client.api_call(
                    "dialog.open",
                    trigger_id=payload["trigger_id"],
                    dialog= dialog
                )
            return make_response("", 200)

        elif payload["callback_id"] == "comment":
            slack_client.api_call(
                "dialog.open",
                trigger_id=payload["trigger_id"],
                dialog=comment_dialog_json.comment_dialog(payload)
            )
            return make_response("", 200)
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
        if payload["callback_id"] == "jamaconnect_comment_dialog_options":
            return comment.comment_dialog_option(payload)
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
    action, content = tools.cutArgument(req.form['text'], ':')
    action = action.strip().lower()
    content = content.strip()

    # See's what kind of arguments there are
    if(action == 'search'):
        print('SEARCH')
        return resolve_search_req(base_url, content)

    elif(action == 'display'):
        print('DISPLAY')
        return resolve_display_req(base_url, content)

    elif (action == 'create'):
        if (content == ""):
            return commands_info.create(request,
            headline="There was an error with your inputs!")

        return create_req.resolve(base_url=base_url, 
                                content=content,
                                slack_client=slack_client,
                                request=request)

    elif (action == 'comment'):
        print('COMMENT')
        return resolve_comment_req(base_url, content)

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

    return make_response("", 400)


### Resolver functions

def resolve_search_req(base_url, content):
    """
    @params:
        base_url -> url to pass down
        content -> contains search key (i.e. "key=some search string")
    """

    try:
        # Make dictionary of the key value pairs encoded in content
        content = make_dict(content)
        # Assigns JSON obj to search result
        search_result = search.search_by_string(base_url, content["key"])
        tools.return_to_slack(request, search_result)
        return make_response("", 200)

    except Exception as e:
        print(e)
        return commands_info.search(request, 
            headline="There was an error with your command! Here is a quick guide to using `/jamaconnect search`:")


def resolve_display_req(base_url, content):
    """
    @params:
        base_url -> url to pass down
        content -> contains search key (i.e. "id=jama item ID")
    """

    try:
        # Make dictionary of the key value pairs encoded in content
        content = make_dict(content)
        # Assigns JSON obj to search result
        search_result = search.search_by_id(base_url, content["id"])
        tools.return_to_slack(request, search_result)
        return make_response("", 200)

    except Exception as e:
        print(e)
        return commands_info.search(request, 
            headline="There was an error with your command! Here is a quick guide to using `/jamaconnect display`:")


def resolve_comment_req(base_url, content):
    """
    @params:
        base_url -> url to pass down
        req -> request to process
    """
    try:
        if content == "":
            slack_client.api_call(
                "dialog.open",
                trigger_id=request.form["trigger_id"],
                dialog=comment_dialog_json.comment_dialog()
            )
        else:
            comment_create_response = comment.comment_inline(request.form['team_id'], request.form['user_id'], base_url, content)
            tools.return_to_slack(request, comment_create_response)
        return make_response("", 200)
    except Exception as e:
        print(e)
        return commands_info.comment(request,
        headline="There was an error with your command! Here is a quick guide to using `/jamaconnect comment`:")


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
