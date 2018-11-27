from jama import api_caller
from slack import tools
from jama.tools import convert_date
from jama.tools import clean_html
import requests
import json
import os
import hmac
import hashlib
import urllib


"""This file contains the central search functionality

There are two main functionaries present in this file:
    1. Receiving formatted data from a dialog in Slack and posting to Jama
    2. Receiving filtered/formatted data from inline interface and posting to Jama

Attributes:
    None
"""

username = os.environ["JAMA_USER"]
password = os.environ["JAMA_PASS"]

def search_by_string(team_id, user_id, base_url, string_to_find):
    """
    Search jama instance for items containing a specific string
    Args:
        base_url (string): The Jama workspace base_url
        team_id (string): Slack team ID
        user_id (string): Slack user ID
        string_to_find (string): the specific string we are searching the jama instance for
    Returns:
        (dict): Returns JSON object to be sent to Slack with description of results and array of results as an attachment, or error message string on failure
    """

    MAX = 10

    # Make sure search string is valid
    if string_to_find == "":
        return {"text": "Please include a search keyword, e.g. \"/jamaconnect search: key=[your search phrase]\"."}
    if len(string_to_find) <= 2:
        return {"text": "Your search keyword must be 3 characters or more."}
    
    # Append search string to base search url and then make request
    url = base_url + "/rest/latest/" + "abstractitems?contains=" + string_to_find
    print("URL:" + url)
    json_response = get(url)
    # json_response = api_caller.get(team_id, user_id, url)
    if json_response is None:
        return {"text": "Failed to authenticate command with OAuth. Try running `/jamaconnect oauth`"}

    data = []
    num_of_result = json_response["meta"]["pageInfo"]["totalResults"]

    if num_of_result > 0:
        max_result = min(num_of_result, MAX)  # Slack allows a max of 20 attachments, max_result allows customizability for result limit
        search_result = json_response["data"]
        # Format each search result and store in the array.
        for i in range(0, max_result):
            buffer = {}
            buffer["title"] = search_result[i]["fields"]["name"]
            buffer["color"] = "#36a64f"
            buffer["title_link"] = base_url + "/perspective.req#/items/" + str(search_result[i]["id"]) + "?projectId="\
                    + str(search_result[i]["project"])
            buffer["text"] = "URL: " + base_url + "/perspective.req#/items/" + str(search_result[i]["id"]) + "?projectId="\
                    + str(search_result[i]["project"])
            buffer["text"] += "\n" + clean_html.remove_tags(search_result[i]["fields"]["description"])
            buffer["footer"] = "Last modified: "
            buffer["ts"] = convert_date.convert(search_result[i]["modifiedDate"])
            data.append(buffer)  # add to array

        # Insert a title about search results in the response
        if num_of_result == 1:
            return_data = {"text": str(num_of_result) + " search result for \"" + str(string_to_find) + "\" :"}
        elif num_of_result <= MAX:
            return_data = {"text": str(num_of_result) + " search results for \"" + str(string_to_find) + "\" :"}
        else:
            return_data = {"text": str(num_of_result) + " search results for \"" + str(string_to_find) + "\" :"}
            return_data["text"] += "\nDisplaying the first " + str(MAX) + " results. View all results here: "\
                    + base_url + "/perspective.req#/search?term=" + urllib.parse.quote_plus(string_to_find)
            "https://capstone-test.jamacloud.com/perspective.req#/search?term=test"
        # Set "attachments" value of response to the array of results and then return it
        return_data["attachments"] = data

        return return_data
    else:
        return {"text": "No results found for \"" + string_to_find + "\"."}

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
    str_to_find = payload["submission"]["key"]
    team_id = payload["team"]["id"]
    user_id = payload["user"]["id"]
    return search_by_string(team_id, user_id, base_url, string_to_find)

def get(url):
    response = requests.get(url, auth=(username, password))
    return json.loads(response.text)
