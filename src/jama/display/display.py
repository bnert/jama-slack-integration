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

def fetch_by_id(team_id, user_id, base_url, id_to_find):
    """
    Search jama instance for the item with a certain ID
    Args:
        base_url (string): The Jama workspace base_url
        team_id (string): Slack team ID
        user_id (string): Slack user ID
        id_to_find (string): the specific id we are searching the jama instance for
    Returns:
        (dict): Returns JSON object to be sent to Slack with description of result and the result as an attachment, or error message string on failure
    """

    if id_to_find == "":
        return {"text": "Please include an item ID, e.g. `/jamaconnect display: <unique jama item ID>`."}
    # Append search string to base search url and then make request
    url = base_url + "/rest/latest/" + "abstractitems/" + id_to_find
    json_response = api_caller.get(team_id, user_id, url)
    if json_response is None:
        return {"text": "Failed to authenticate command with OAuth. Try running `/jamaconnect oauth`"}

    data = []

    # Format the search result and store in the array (stored in array to match the formatting of search by ID)
    if json_response["meta"]["status"] == "OK":
        search_result = json_response["data"]

        buffer = {}
        buffer["title"] = "Item #" + id_to_find + ": " + search_result["fields"]["name"]
        buffer["color"] = "#36a64f"
        buffer["title_link"] = base_url + "/perspective.req#/items/" + str(search_result["id"]) + "?projectId="\
                + str(search_result["project"])
        buffer["text"] = "URL: " + base_url + "/perspective.req#/items/" + str(search_result["id"]) + "?projectId="\
                + str(search_result["project"])
        buffer["text"] += "\nProject: " + str(search_result["project"])
        buffer["text"] += "\n" + clean_html.remove_tags(search_result["fields"]["description"])
        buffer["footer"] = "Last modified: "
        buffer["ts"] = convert_date.convert(search_result["modifiedDate"])
        data.append(buffer)  # add to array

        # Set "attachments" value of response to the array of results and then return it
        return_data = {"text": ""}
        return_data["attachments"] = data
        return return_data
    else:
        return {"text": "No item found with ID: " + id_to_find}

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
    id_to_find = payload["submission"]["id"]
    team_id = payload["team"]["id"]
    user_id = payload["user"]["id"]
    return fetch_by_id(team_id, user_id, base_url, id_to_find)
