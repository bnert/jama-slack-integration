from dateutil.parser import parse
import xml.etree.ElementTree as ET
import requests
import json
import os
import time
import hmac
import hashlib
import urllib
import re


username = os.environ["JAMA_USER"]
password = os.environ["JAMA_PASS"]


def search_by_string(base_url, string_to_find):
    """
    @params:
        base_url -> Jama url to build API call url off of
        string_to_find -> search key string
    @returns:
        return_data -> object to be sent to Slack with description of results and array of results as an attachment, or error message string on failure
    """
    MAX = 10;

    # Make sure search string is valid
    if string_to_find == "":
        return {"text": "Please include a search keyword, e.g. \"/jamaconnect search: key=[your search phrase]\"."}
    if len(string_to_find) <= 2:
        return {"text": "Your search keyword must be 3 characters or more."}
    
    # Append search string to base search url and then make request
    url = base_url + "/rest/latest/" + "abstractitems?contains=" + string_to_find
    json_response = get(url)
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
            buffer["text"] += "\n" + remove_tags(search_result[i]["fields"]["description"])
            buffer["footer"] = "Last modified at "
            buffer["ts"] = to_epoch_time(search_result[i]["modifiedDate"])
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


def search_by_id(base_url, id_to_find):
    """
    @params:
        base_url -> Jama url to build API call url off of
        id_to_find -> item id string
    @returns:
        return_data -> object to be sent to Slack with description of result and the result as an attachment, or error message string on failure
    """
    if id_to_find == "":
        return {"text": "Please include an item ID, e.g. \"/jamaconnect search: id=[unique jama item ID]\"."}
    # Append search string to base search url and then make request
    url = base_url + "/rest/latest/" + "abstractitems/" + id_to_find
    json_response = get(url)
    data = []

    # Format the search result and store in the array (stored in array to match the formatting of search by ID)
    if json_response["meta"]["status"] == "OK":
        search_result = json_response["data"]

        buffer = {}
        buffer["title"] = search_result["fields"]["name"]
        buffer["color"] = "#36a64f"
        buffer["title_link"] = base_url + "/perspective.req#/items/" + str(search_result["id"]) + "?projectId="\
                + str(search_result["project"])
        buffer["text"] = "URL: " + base_url + "/perspective.req#/items/" + str(search_result["id"]) + "?projectId="\
                + str(search_result["project"])
        buffer["text"] += "\n" + remove_tags(search_result["fields"]["description"])
        buffer["footer"] = "Last modified at "
        buffer["ts"] = to_epoch_time(search_result["modifiedDate"])
        data.append(buffer)  # add to array

        # Insert a title about search results in the response
        return_data = {"text": " Displaying item with ID: " + id_to_find + ":"}
        # Set "attachments" value of response to the array of results and then return it
        return_data["attachments"] = data
        return return_data
    else:
        return {"text": "No item found with ID: " + id_to_find}


def remove_tags(text):
    text = re.sub("<[^<]+?>", "", text)
    text = re.sub("&nbsp;", " ", text)
    text = re.sub("&quot;", "\"", text)
    text = re.sub("&apos;", "'", text)
    text = re.sub("&gt;", "<", text)
    return re.sub("&lt;", ">", text)

def get(url):
    response = requests.get(url, auth=(username, password))
    return json.loads(response.text)

def to_epoch_time(date):
    date_time = parse(date)
    return date_time.timestamp()
