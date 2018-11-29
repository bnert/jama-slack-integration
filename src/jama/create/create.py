import os
import json
import requests
from flask import make_response
from jama.json_factories import item_factory
from jama import oauth
from jama import api_caller
from slack.slack_json_factories.resp_json import created_item
from slack import tools
from pprint import pprint

"""create.py == Backbone of create functionality

There are two main functionalities present in this file:
    1. Recieving formatted data from a dialog in Slack and posting to Jama
    2. Recieving filtered/formatted data from text interface and posting to Jama

As the file name is states, these functions are the backbone for the ability to create
an item from data that is input in Slack.

Attributes:
    None
"""

def from_dialog(url_base, json_to_parse):
    """Creates a Jama item from dialog submission.
    
    Args:
        url_base (string): base url for jama instance
        json_to_parse (string): slack json submission

    Returns:
        (dict): Returns JSON object with created item url and status
    Raises:
        Exception:
            Raised if there is a problem parsing dialog data
    """
    try:
        sub_data = json_to_parse["submission"]
        team_id = json_to_parse["team"]["id"]
        user_id = json_to_parse["user"]["id"]
        jama_url = url_base + '/rest/latest/items?setGlobalIdManually=false'

        to_post_obj = item_factory.generate_item()        
        parentId, projectId, item_type = sub_data["projectId"].split('.')
        to_post_obj["project"] = int(projectId)
        to_post_obj["location"]["parent"]["item"] = int(parentId)
        to_post_obj["itemType"] = int(item_type)
        to_post_obj["fields"]["name"] = sub_data["newItemName"]
        to_post_obj["fields"]["description"] = sub_data["description"]

        jama_resp = api_caller.post(team_id, user_id, jama_url, payload=to_post_obj)
        if jama_resp is None:
            raise Exception("Invaid oauth credentials")

        return created_item.resp_json(jama_resp, to_post_obj["project"])
    except Exception as err:
        print(err)
        if "oauth" in err:    
            err_msg = {
                "text": "{oauth_err}".format(oauth_err=err),
                "attachments": [
                    {
                        "text": """Please update your oauth credentials and give it another go!
                        If it doens't work, please submit a bug report"""
                    }
                ]
            }
        else:
            err_msg = {
                    "text": "We're sorry, we had trouble handling your data",
                    "attachments": [
                        {
                            "text": """Please give it another go!
                            If it doens't work, please submit a bug report"""
                        }
                    ]
                }
        return make_response(err_msg, 500)



def from_text(base_url, content_dict, team_id, user_id):
    """Create a item to be passed to Jama API
    
    Args:
        base_url (string): Jama instance URL, used to send data to Jama
        content_dict (dict): key value pairs with parameters to create item.
        
    Returns:
        (dict): Returns JSON object with created item url and status
    Raises:
        Exception:
            Raised if there is a problem parsing dialog data  
    """
    # If dict is empty, means there is a parse error
    if not bool(content_dict):
        return {
            "text": "Oh no, there was an error with your inputs!",
            "attachments": [
                {
                    "text": """Example usage of `/jamaconnect create`:
\t`/jamaconnect create: <projectId>` brings up a dialog for
\t\t\tthe top level items for the specified project, given the project's ID.
\t---- or -----
\t`/jamaconnect create: project=<projectID> | name=project name | ...` will
\t\t\talso work, where `...` is other arguments, such as: `item=<itemID>`, or
\t\t\t`description=your item description`.

*Note: all fields with `<...>` around them are places you need to provide input. 
If a field is an ID (e.g. projectID), it needs to be a number. Otherwise, it can be text.*
                    """
                }
            ]
        }

    # Gets JSON structure for a jama item
    to_post_obj = item_factory.generate_item()

    try:
        for key in content_dict:
            # Some keys need to be ints
            # specifically project, item, itemType
            if key in to_post_obj:
                if key != 'project' or key != 'item':
                    to_post_obj[key] = int(content_dict[key]) if key == 'itemType' else content_dict[key]
            else:
                to_post_obj["fields"][key] = content_dict[key]

        # Check to see if an item is specified
        # If so, use it
        # If not, use project as parent
        if "item" in content_dict:
            to_post_obj["location"]["parent"]["item"] = int(content_dict["item"])
        elif "project" in content_dict:
            to_post_obj["location"]["parent"]["project"] = int(content_dict["project"])
            to_post_obj["location"]["parent"].pop("item")
    except Exception:
        return {
            "text": "Oh no, there was an error with your inputs!",
            "attachments": [
                {
                    "text": """Example usage of `/jamaconnect create`:
\t`/jamaconnect create: <projectId>` brings up a dialog for
\t\t\tthe top level items for the specified project, given the project's ID.
\t---- or -----
\t`/jamaconnect create: project=<projectID> | name=project name | ...` will
\t\t\talso work, where `...` is other arguments, such as: `item=<itemID>`, or
\t\t\t`description=your item description`.

*Note: all fields with `<...>` around them are places you need to provide input. 
If a field is an ID (e.g. projectID), it needs to be a number. Otherwise, it can be text.*
                    """
                }
            ]
        }

    jama_url = base_url + '/rest/latest/items/'
    jama_resp = api_caller.post(team_id, user_id, jama_url, payload=to_post_obj)
    if jama_resp is None:
        raise Exception("Invaid oauth credentials")

    # Returns json object w/ url of new item
    return created_item.resp_json(jama_resp, to_post_obj["project"])
