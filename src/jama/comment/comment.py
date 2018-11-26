import json
from flask import make_response
from jama.json_factories import comment_factory
from jama import api_caller
from slack.slack_json_factories.resp_json.comment import comment_response
from slack import tools
from jama import tools as jama_tools

"""comment.py == Backbone of comment functionality

There are two main functionaries present in this file:
    1. Receiving formatted data from a dialog in Slack and posting to Jama
    2. Receiving filtered/formatted data from inline interface and posting to Jama

As the file name is states, these functions are the backbone for the ability to create
an item from data that is input in Slack.

Attributes:
    None
"""

# Temporary store users that is using the comment dialog
user_project_id_list = {}


def from_dialog(base_url, payload):
    """
    Prepare the payload from slack
    Remove the user from the list after they hit submit
    Comment at jama site

    Args:
        base_url (string): jama instance base url
        payload (dict): payload receive from slack
    Returns:
        (dict): Returns JSON object with comment item url and status
    """
    global user_project_id_list
    post_id = payload["submission"]["item"]
    comment_body = payload["submission"]["comment"]
    slack_team_id = payload["team"]["id"]
    slack_user_id = payload["user"]["id"]
    if (slack_team_id, slack_user_id) in user_project_id_list:
        del user_project_id_list[(slack_team_id, slack_user_id)]
    return comment(base_url, slack_team_id, slack_user_id, post_id, comment_body)


def from_inline(slack_team_id, slack_user_id, base_url, args):
    """
    Process input from slack massage and sent them to comment()
    Args:
        slack_team_id (string): The slack team ID
        slack_user_id (string): The slack User ID, which is not the username!
        base_url (string): The Jama workspace base_url
        args (dict): the user input content which is cut at routes.py
    Returns:
        (dict): Returns JSON object with commented item url and status
    """
    # str_post_id, comment_body = tools.cutArgument(content, ",")
    return comment(base_url, slack_team_id, slack_user_id, args["id"], args["comment"])


def comment(base_url, team_id, user_id, str_post_id, comment_body):
    """
    Comment by passing URL routes with query string
    Args:
        base_url (string): The Jama workspace base_url
        team_id (string): Slack team ID
        user_id (string): Slack user ID
        str_post_id (string): a string format item id, which is the item user want to comment
        comment_body (string): the context user want to put into the comment
    Returns:
        (dict): Returns JSON object with commented item url and status
    """
    post_id = tools.string_to_int(str_post_id)
    if post_id < 0 or comment_body == "":
        return comment_response(str_post_id, comment_body)

    if api_caller.is_using_oauth():
        header = ""
    else:
        header = jama_tools.prepare_writer_info(team_id, user_id, base_url, True)
    comment_body = comment_body
    obj = comment_factory.generate_comment(post_id, tools.prepare_html(header + comment_body))
    url = base_url + "/rest/latest/comments"
    response = api_caller.post(team_id, user_id, url, obj)

    return comment_response(str_post_id, comment_body, response)


def dialog_option(base_url, json_request):
    """
    Handle dynamic options menu for dialog
    Args:
        base_url (string): The Jama workspace base_url
        json_request (dict): Slack team ID
    Returns:
        (dict): Returns JSONed object of options to slack
    """
    value = json_request["value"]
    teamID = json_request["team"]["id"]
    userID = json_request["user"]["id"]
    state = json_request["state"]
    if json_request["name"] == "project":
        return dynamic_project_list(base_url, value, teamID, userID)
    elif json_request["name"] == "project_id":
        return dynamic_search_project(base_url, value, teamID, userID)
    elif json_request["name"] == "item":
        return dynamic_item_list(base_url, value, teamID, userID, state)
    else:
        return make_response("", 500)


def dynamic_project_list(base_url, keyword, teamID, userID):
    """
    Fetch all the project from jama
    If user give empty input, shows first up to 100 projects
    If user enter keyword, search projects name using that keyword
    Args:
        base_url (string): The Jama workspace base_url
        keyword (string): keyword of the project
        teamID (string): Slack team ID
        userID (string): Slack user ID
    Returns:
        (dict): Returns JSONed object of options to slack
    """
    options = []
    jama_json_response = jama_tools.get_projectID(base_url, 0, teamID, userID)
    total_results = jama_json_response["meta"]["pageInfo"]["totalResults"]
    result_count = jama_json_response["meta"]["pageInfo"]["resultCount"]
    index = 0
    while True:
        for i in range(0, result_count):
            buffer = {}
            buffer["label"] = str(jama_json_response["data"][i]["id"]) + ": " + jama_json_response["data"][i]["fields"][
                "name"]
            buffer["value"] = jama_json_response["data"][i]["id"]
            options.append(buffer)  # add to array
        index += 50
        if index >= total_results:
            break
        jama_json_response = jama_tools.get_projectID(base_url, index, teamID, userID)
        result_count = jama_json_response["meta"]["pageInfo"]["resultCount"]
        
    if keyword == "":
        slack_payload = {
            "options": options[:100]
        }
        return make_response(json.dumps(slack_payload), 200)
    else:
        options_filtered = []
        keyword = keyword.lower()
        for j in range(0, len(options)):
            if keyword in options[j]["label"].lower():
                options_filtered.append(options[j])
        slack_payload = {
            "options": options_filtered[:100]
        }
        return make_response(json.dumps(slack_payload), 200)


def dynamic_search_project(base_url, keyword, teamID, userID):
    """
    conform project
    user enter the project id, and search that project from jama
    Args:
        base_url (string): The Jama workspace base_url
        keyword (string): keyword of the project
        teamID (string): Slack team ID
        userID (string): Slack user ID
    Returns:
        (dict): Returns JSONed object of options to slack
    """
    global user_project_id_list
    if keyword:
        jama_json_response = jama_tools.get_project_by_ID(base_url, keyword, teamID, userID)
        if jama_json_response["meta"]["status"] == "OK":
            user_project_id_list[(teamID, userID)] = keyword
            options = []  # Show optins on Slack dialog
            buffer = {}
            buffer["label"] = str(jama_json_response["data"]["id"]) + ": " + jama_json_response["data"]["fields"][
                "name"]
            buffer["value"] = jama_json_response["data"]["id"]
            options.append(buffer)  # add to array
            slack_payload = {
                "options": options[:100]
            }
            return make_response(json.dumps(slack_payload), 200)
    return make_response("", 500)


def dynamic_item_list(base_url, keyword, teamID, userID, state):
    """
    If no user input, show first 50 items
    IF user input number, search item using it as item id
    IF user input something else, search item name with that keyword
    Args:
        base_url (string): The Jama workspace base_url
        keyword (string): keyword of the item
        teamID (string): Slack team ID
        userID (string): Slack user ID
    Returns:
        (dict): Returns JSONed object of options to slack
    """
    global user_project_id_list
    if keyword == "":
        """
        No user input, show the first 50 items
        """
        if (teamID, userID) in user_project_id_list:
            project_id = user_project_id_list[(teamID, userID)]
        elif not state == "":
            project_id = state
        else:
            return make_response("", 500)
        jama_json_response = jama_tools.get_item(base_url, project_id, 0, teamID, userID)
        if jama_json_response["meta"]["status"] == "OK":
            options = []
            total_results = jama_json_response["meta"]["pageInfo"]["totalResults"]
            result_count = jama_json_response["meta"]["pageInfo"]["resultCount"]
            if total_results > 0:
                for i in range(0, result_count):
                    buffer = {}
                    buffer["label"] = str(jama_json_response["data"][i]["id"]) + ": " + \
                                      jama_json_response["data"][i]["fields"]["name"]
                    buffer["value"] = jama_json_response["data"][i]["id"]
                    options.append(buffer)
                slack_payload = {
                    "options": options[:100]
                }
                return make_response(json.dumps(slack_payload), 200)

    elif tools.string_to_int(keyword) >= 0:
        """
        User types in number for item ID for item in Jama.
        """
        jama_json_response = jama_tools.get_item_by_ID(base_url, keyword, teamID, userID)
        if jama_json_response["meta"]["status"] == "OK":
            options = []  # Show optins on Slack dialog
            buffer = {}
            buffer["label"] = str(jama_json_response["data"]["id"]) + ": " + jama_json_response["data"]["fields"][
                "name"]
            buffer["value"] = jama_json_response["data"]["id"]
            options.append(buffer)  # add to array
            slack_payload = {
                "options": options[:100]
            }
            return make_response(json.dumps(slack_payload), 200)
        else:
            return make_response("", 500)

    else:
        """
        user input keyword
        Search item with the user input
        Load the result, and only return the item with keywort in its name
        """
        if (teamID, userID) in user_project_id_list:
            project_id = user_project_id_list[(teamID, userID)]
        elif not state == "":
            project_id = state
        else:
            return make_response("", 500)
        keyword = keyword.lower()
        jama_json_response = jama_tools.search_item(base_url, project_id, 0, keyword, teamID, userID)
        result_count = jama_json_response["meta"]["pageInfo"]["resultCount"]
        total_results = jama_json_response["meta"]["pageInfo"]["totalResults"]
        index = 0
        options_filtered = []
        while True:
            for i in range(0, result_count):
                if not keyword in jama_json_response["data"][i]["fields"]["name"].lower():
                    continue
                buffer = {}
                buffer["label"] = str(jama_json_response["data"][i]["id"]) + ": " + \
                                  jama_json_response["data"][i]["fields"]["name"]
                buffer["value"] = jama_json_response["data"][i]["id"]
                options_filtered.append(buffer) 
            index += 50
            if index >= total_results:
                break
            jama_json_response = jama_tools.search_item(base_url, project_id, index, keyword)
            result_count = jama_json_response["meta"]["pageInfo"]["resultCount"]
        slack_payload = {
            "options": options_filtered[:100]
        }
        return make_response(json.dumps(slack_payload), 200)
    return make_response("", 500)
