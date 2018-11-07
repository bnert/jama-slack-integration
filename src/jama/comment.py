import json
from flask import make_response, Response
import os
from jama.json_factories import comment_factory
from jama import api_caller
from slack.slack_json_factories.comment_response_json import comment_response
from slack import tools

# Temporary store users that is using the comment dialog
user_project_id_list = {}

def from_dialog_comment(base_url, payload):
    """
    Prepare the paylaod from slack
    Remove the user from the list after they hit submit
    Comment at jama site

    @params:
        base_url -> jama instance base url
        payload -> payload receive from slack
    """
    global user_project_id_list
    post_id = payload["submission"]["item"]
    comment_body = payload["submission"]["comment"]
    slack_team_id = payload["team"]["id"]
    slack_user_id = payload["user"]["id"]
    if (slack_team_id, slack_user_id) in user_project_id_list:
        del user_project_id_list[(slack_team_id, slack_user_id)]
    return comment(base_url, slack_team_id, slack_user_id, post_id, comment_body)

def get_projectID(base_url, start, teamID, userID):
    """
    Get all the project from jama

    @params:
        base_url -> jama instance base url
        start -> start at a specific location
        teamID -> user team ID, for OAuth
        userID -> user ID, for OAuth
    """
    url = base_url + "/rest/latest/projects?startAt=" +\
          str(start) + "&maxResults=50"
    return api_caller.get(teamID, userID, url)

def get_project_by_ID(base_url, projectID, teamID, userID):
    """
    Get the project from jama by project id

    @params: 
        base_url -> jama instance base url
        projectID -> project id
        teamID -> user team ID, for OAuth
        userID -> user ID, for OAuth
    """
    url = base_url + "/rest/latest/projects/" + projectID
    return api_caller.get(teamID, userID, url)

def get_item_by_ID(base_url, itemID, teamID, userID):
    """
    Get the item from jama by item id

    @params: 
        base_url -> jama instance base url
        itemID -> item id
        teamID -> user team ID, for OAuth
        userID -> user ID, for OAuth
    """
    url = base_url + "/rest/latest/abstractitems/" + itemID
    return api_caller.get(teamID, userID, url)

def get_item(base_url, projectID, start, teamID, userID):
    """
    Get all the item from a project

    @params: 
        base_url -> jama instance base url
        projectID -> project id
        start -> start at a specific index
        teamID -> user team ID, for OAuth
        userID -> user ID, for OAuth
    """
    url = base_url + "/rest/latest/items?project=" + str(projectID) +\
          "&startAt=" + str(start) + "&maxResults=50"
    return api_caller.get(teamID, userID, url)

def search_item(base_url, projectID, start, contains, teamID, userID):
    """
    Search a item from a project

    @params: 
        base_url -> jama instance base url
        projectID -> project id
        start -> start at a specific index
        contains -> the keyword
        teamID -> user team ID, for OAuth
        userID -> user ID, for OAuth
    """
    url = base_url + "/rest/latest/abstractitems?project=" +\
          str(projectID) + "&contains=" + contains + "&startAt=" + str(start) + "&maxResults=50"
    return api_caller.get(teamID, userID, url)

def comment_from_commandline(slack_team_id, slack_user_id, base_url, content):
    """
    Process input from slack massage and sent them to comment()
    @params:
        slack_team_id -> The slack team ID
        slack_user_id -> The slack User ID, which is not the username!
        base_url -> The Jama workspace base_url
        content -> the user input content which is cut at routes.py
    """
    str_post_id, comment_body = tools.cutArgument(content, ",")
    return comment(base_url, slack_team_id, slack_user_id, str_post_id, comment_body)

def comment(base_url, team_id, user_id, str_post_id, comment_body):
    """
    Comment by passing URL routes with query string
    @params:
        base_url -> The Jama workspace base_url
        team_id -> Slack team ID
        user_id -> Slack user ID
        str_post_id -> a string format item id, which is the item user want to comment
        comment_body -> the context user want to put into the comment
    """
    post_id = tools.string_to_int(str_post_id)
    if post_id < 0 or comment_body == "":
        return comment_response(str_post_id, comment_body)
    obj = comment_factory.generate_comment(post_id, tools.prepare_html(comment_body))
    url = base_url + "/rest/latest/comments"
    response = api_caller.post(team_id, user_id, url, obj)

    return comment_response(str_post_id, comment_body, response)
    
def comment_inline(base_url, json_request):
    """
    Handle dynamic options menu for dialog
    """
    value = json_request["value"]
    teamID = json_request["team"]["id"]
    userID = json_request["user"]["id"]
    if json_request["name"] == "project":
        return dynamic_project_list(base_url, value, teamID, userID)
    elif json_request["name"] == "project_id":
        return dynamic_search_project(base_url, value, teamID, userID)
    elif json_request["name"] == "item":
        return dynamic_item_list(base_url, value, teamID, userID)
    else:
        return make_response("", 500)

def dynamic_project_list(base_url, keyword, teamID, userID):
    """
    Fetch all the project from jama
    If user give empty input, shows first up to 100 projects
    If user enter keyword, search projects name using that keyword
    """
    options = []
    jama_json_response = get_projectID(base_url, 0, teamID, userID)
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
        jama_json_response = get_projectID(base_url, index, teamID, userID)
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
    return make_response("", 200)

def dynamic_search_project(base_url, keyword, teamID, userID):
    """
    conform project
    user enter the project id, and search that project from jama
    """
    global user_project_id_list
    if keyword:
        jama_json_response = get_project_by_ID(base_url, keyword, teamID, userID)
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


def dynamic_item_list(base_url, keyword, teamID, userID):
    """
    If no user input, show first 50 items
    IF user input number, search item using it as item id
    IF user input something else, search item name with that keyword
    """
    global user_project_id_list
    if keyword == "":
        """
        No user input, show the first 50 items
        """
        if not (teamID, userID) in user_project_id_list:
            return make_response("", 500)
        project_id = user_project_id_list[(teamID, userID)]
        jama_json_response = get_item(base_url, project_id, 0, teamID, userID)
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
        jama_json_response = get_item_by_ID(base_url, keyword, teamID, userID)
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
        if not (teamID, userID) in user_project_id_list:
            return make_response("", 500)
        project_id = user_project_id_list[(teamID, userID)]
        keyword = keyword.lower()
        jama_json_response = search_item(base_url, project_id, 0, keyword, teamID, userID)
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
            jama_json_response = search_item(base_url, project_id, index, keyword)
            result_count = jama_json_response["meta"]["pageInfo"]["resultCount"]
        slack_payload = {
            "options": options_filtered[:100]
        }
        return make_response(json.dumps(slack_payload), 200)
    return make_response("", 500)
